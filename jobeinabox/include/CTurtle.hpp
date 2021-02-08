/*Include GIF utility when compiling headless mode.*/
/*License for CTurtle itself is found further down in the file.
 * Ctrl+F for "MIT" should get you there.*/

#define CTURTLE_HEADLESS
#ifdef CTURTLE_HEADLESS

/* public domain, Simple, Minimalistic GIF writer - http://jonolick.com
 *
 * Quick Notes:
 * 	Supports only 4 component input, alpha is currently ignored. (RGBX)
 *
 * Latest revisions:
 * 	1.00 (2015-11-03) initial release
 *
 * Basic usage:
 *	char *frame = new char[128*128*4]; // 4 component. RGBX format, where X is unused
 *	jo_gif_t gif = jo_gif_start("foo.gif", 128, 128, 0, 32);
 *	jo_gif_frame(&gif, frame, 4, false); // frame 1
 *	jo_gif_frame(&gif, frame, 4, false); // frame 2
 *	jo_gif_frame(&gif, frame, 4, false); // frame 3, ...
 *	jo_gif_end(&gif);
 * */

#ifndef JO_INCLUDE_GIF_H
#define JO_INCLUDE_GIF_H

#include <stdio.h>

//Header edited to inline all GIF functionality to avoid re-definitions across compilation units
//otherwise, left the same.

typedef struct {
    FILE *fp;
    unsigned char palette[0x300];
    short width, height, repeat;
    int numColors, palSize;
    int frame;
} jo_gif_t;

// width/height	| the same for every frame
// repeat       | 0 = loop forever, 1 = loop once, etc...
// palSize		| must be power of 2 - 1. so, 255 not 256.
inline jo_gif_t jo_gif_start(const char *filename, short width, short height, short repeat, int palSize);

// gif			| the state (returned from jo_gif_start)
// rgba         | the pixels
// delayCsec    | amount of time in between frames (in centiseconds)
// localPalette | true if you want a unique palette generated for this frame (does not effect future frames)
inline void jo_gif_frame(jo_gif_t *gif, unsigned char *rgba, short delayCsec, bool localPalette);

// gif          | the state (returned from jo_gif_start)
inline void jo_gif_end(jo_gif_t *gif);

#if defined(_MSC_VER) && _MSC_VER >= 0x1400
#define _CRT_SECURE_NO_WARNINGS // suppress warnings about fopen()
#endif

#include <stdlib.h>
#include <memory.h>
#include <math.h>

// Based on NeuQuant algorithm
inline void jo_gif_quantize(unsigned char *rgba, int rgbaSize, int sample, unsigned char *map, int numColors) {
    // defs for freq and bias
    const int intbiasshift = 16; /* bias for fractions */
    const int intbias = (((int) 1) << intbiasshift);
    const int gammashift = 10; /* gamma = 1024 */
    const int betashift = 10;
    const int beta = (intbias >> betashift); /* beta = 1/1024 */
    const int betagamma = (intbias << (gammashift - betashift));

    // defs for decreasing radius factor
    const int radiusbiasshift = 6; /* at 32.0 biased by 6 bits */
    const int radiusbias = (((int) 1) << radiusbiasshift);
    const int radiusdec = 30; /* factor of 1/30 each cycle */

    // defs for decreasing alpha factor
    const int alphabiasshift = 10; /* alpha starts at 1.0 */
    const int initalpha = (((int) 1) << alphabiasshift);

    // radbias and alpharadbias used for radpower calculation
    const int radbiasshift = 8;
    const int radbias = (((int) 1) << radbiasshift);
    const int alpharadbshift = (alphabiasshift + radbiasshift);
    const int alpharadbias = (((int) 1) << alpharadbshift);

    sample = sample < 1 ? 1 : sample > 30 ? 30 : sample;
    int network[256][3];
    int bias[256] = {}, freq[256];
    for(int i = 0; i < numColors; ++i) {
        // Put nurons evenly through the luminance spectrum.
        network[i][0] = network[i][1] = network[i][2] = (i << 12) / numColors;
        freq[i] = intbias / numColors;
    }
    // Learn
    {
        const int primes[5] = {499, 491, 487, 503};
        int step = 4;
        for(int i = 0; i < 4; ++i) {
            if(rgbaSize > primes[i] * 4 && (rgbaSize % primes[i])) { // TODO/Error? primes[i]*4?
                step = primes[i] * 4;
            }
        }
        sample = step == 4 ? 1 : sample;

        int alphadec = 30 + ((sample - 1) / 3);
        int samplepixels = rgbaSize / (4 * sample);
        int delta = samplepixels / 100;
        int alpha = initalpha;
        delta = delta == 0 ? 1 : delta;

        int radius = (numColors >> 3) * radiusbias;
        int rad = radius >> radiusbiasshift;
        rad = rad <= 1 ? 0 : rad;
        int radSq = rad*rad;
        int radpower[32];
        for (int i = 0; i < rad; i++) {
            radpower[i] = alpha * (((radSq - i * i) * radbias) / radSq);
        }

        // Randomly walk through the pixels and relax neurons to the "optimal" target.
        for(int i = 0, pix = 0; i < samplepixels;) {
            int r = rgba[pix + 0] << 4;
            int g = rgba[pix + 1] << 4;
            int b = rgba[pix + 2] << 4;
            int j = -1;
            {
                // finds closest neuron (min dist) and updates freq
                // finds best neuron (min dist-bias) and returns position
                // for frequently chosen neurons, freq[k] is high and bias[k] is negative
                // bias[k] = gamma*((1/numColors)-freq[k])

                int bestd = 0x7FFFFFFF, bestbiasd = 0x7FFFFFFF, bestpos = -1;
                for (int k = 0; k < numColors; k++) {
                    int *n = network[k];
                    int dist = abs(n[0] - r) + abs(n[1] - g) + abs(n[2] - b);
                    if (dist < bestd) {
                        bestd = dist;
                        bestpos = k;
                    }
                    int biasdist = dist - ((bias[k]) >> (intbiasshift - 4));
                    if (biasdist < bestbiasd) {
                        bestbiasd = biasdist;
                        j = k;
                    }
                    int betafreq = freq[k] >> betashift;
                    freq[k] -= betafreq;
                    bias[k] += betafreq << gammashift;
                }
                freq[bestpos] += beta;
                bias[bestpos] -= betagamma;
            }

            // Move neuron j towards biased (b,g,r) by factor alpha
            network[j][0] -= (network[j][0] - r) * alpha / initalpha;
            network[j][1] -= (network[j][1] - g) * alpha / initalpha;
            network[j][2] -= (network[j][2] - b) * alpha / initalpha;
            if (rad != 0) {
                // Move adjacent neurons by precomputed alpha*(1-((i-j)^2/[r]^2)) in radpower[|i-j|]
                int lo = j - rad;
                lo = lo < -1 ? -1 : lo;
                int hi = j + rad;
                hi = hi > numColors ? numColors : hi;
                for(int jj = j+1, m=1; jj < hi; ++jj) {
                    int a = radpower[m++];
                    network[jj][0] -= (network[jj][0] - r) * a / alpharadbias;
                    network[jj][1] -= (network[jj][1] - g) * a / alpharadbias;
                    network[jj][2] -= (network[jj][2] - b) * a / alpharadbias;
                }
                for(int k = j-1, m=1; k > lo; --k) {
                    int a = radpower[m++];
                    network[k][0] -= (network[k][0] - r) * a / alpharadbias;
                    network[k][1] -= (network[k][1] - g) * a / alpharadbias;
                    network[k][2] -= (network[k][2] - b) * a / alpharadbias;
                }
            }

            pix += step;
            pix = pix >= rgbaSize ? pix - rgbaSize : pix;

            // every 1% of the image, move less over the following iterations.
            if(++i % delta == 0) {
                alpha -= alpha / alphadec;
                radius -= radius / radiusdec;
                rad = radius >> radiusbiasshift;
                rad = rad <= 1 ? 0 : rad;
                radSq = rad*rad;
                for (j = 0; j < rad; j++) {
                    radpower[j] = alpha * ((radSq - j * j) * radbias / radSq);
                }
            }
        }
    }
    // Unbias network to give byte values 0..255
    for (int i = 0; i < numColors; i++) {
        map[i*3+0] = network[i][0] >>= 4;
        map[i*3+1] = network[i][1] >>= 4;
        map[i*3+2] = network[i][2] >>= 4;
    }
}

typedef struct {
    FILE *fp;
    int numBits;
    unsigned char buf[256];
    unsigned char idx;
    unsigned tmp;
    int outBits;
    int curBits;
} jo_gif_lzw_t;

inline void jo_gif_lzw_write(jo_gif_lzw_t *s, int code) {
    s->outBits |= code << s->curBits;
    s->curBits += s->numBits;
    while(s->curBits >= 8) {
        s->buf[s->idx++] = s->outBits & 255;
        s->outBits >>= 8;
        s->curBits -= 8;
        if (s->idx >= 255) {
            putc(s->idx, s->fp);
            fwrite(s->buf, s->idx, 1, s->fp);
            s->idx = 0;
        }
    }
}

inline void jo_gif_lzw_encode(unsigned char *in, int len, FILE *fp) {
    jo_gif_lzw_t state = {fp, 9};
    int maxcode = 511;

    // Note: 30k stack space for dictionary =|
    const int hashSize = 5003;
    short codetab[hashSize];
    int hashTbl[hashSize];
    memset(hashTbl, 0xFF, sizeof(hashTbl));

    jo_gif_lzw_write(&state, 0x100);

    int free_ent = 0x102;
    int ent = *in++;
    CONTINUE:
    while (--len) {
        int c = *in++;
        int fcode = (c << 12) + ent;
        int key = (c << 4) ^ ent; // xor hashing
        while(hashTbl[key] >= 0) {
            if(hashTbl[key] == fcode) {
                ent = codetab[key];
                goto CONTINUE;
            }
            ++key;
            key = key >= hashSize ? key - hashSize : key;
        }
        jo_gif_lzw_write(&state, ent);
        ent = c;
        if(free_ent < 4096) {
            if(free_ent > maxcode) {
                ++state.numBits;
                if(state.numBits == 12) {
                    maxcode = 4096;
                } else {
                    maxcode = (1<<state.numBits)-1;
                }
            }
            codetab[key] = free_ent++;
            hashTbl[key] = fcode;
        } else {
            memset(hashTbl, 0xFF, sizeof(hashTbl));
            free_ent = 0x102;
            jo_gif_lzw_write(&state, 0x100);
            state.numBits = 9;
            maxcode = 511;
        }
    }
    jo_gif_lzw_write(&state, ent);
    jo_gif_lzw_write(&state, 0x101);
    jo_gif_lzw_write(&state, 0);
    if(state.idx) {
        putc(state.idx, fp);
        fwrite(state.buf, state.idx, 1, fp);
    }
}

inline int jo_gif_clamp(int a, int b, int c) { return a < b ? b : a > c ? c : a; }

jo_gif_t jo_gif_start(const char *filename, short width, short height, short repeat, int numColors) {
    numColors = numColors > 255 ? 255 : numColors < 2 ? 2 : numColors;
    jo_gif_t gif = {};
    gif.width = width;
    gif.height = height;
    gif.repeat = repeat;
    gif.numColors = numColors;
    gif.palSize = log2(numColors);

    gif.fp = fopen(filename, "wb");
    if(!gif.fp) {
        printf("Error: Could not WriteGif to %s\n", filename);
        return gif;
    }

    fwrite("GIF89a", 6, 1, gif.fp);
    // Logical Screen Descriptor
    fwrite(&gif.width, 2, 1, gif.fp);
    fwrite(&gif.height, 2, 1, gif.fp);
    putc(0xF0 | gif.palSize, gif.fp);
    fwrite("\x00\x00", 2, 1, gif.fp); // bg color index (unused), aspect ratio
    return gif;
}

inline void jo_gif_frame(jo_gif_t *gif, unsigned char * rgba, short delayCsec, bool localPalette) {
    if(!gif->fp) {
        return;
    }
    short width = gif->width;
    short height = gif->height;
    int size = width * height;

    unsigned char localPalTbl[0x300];
    unsigned char *palette = gif->frame == 0 || !localPalette ? gif->palette : localPalTbl;
    if(gif->frame == 0 || localPalette) {
        jo_gif_quantize(rgba, size*4, 1, palette, gif->numColors);
    }

    unsigned char *indexedPixels = (unsigned char *)malloc(size);
    {
        unsigned char *ditheredPixels = (unsigned char*)malloc(size*4);
        memcpy(ditheredPixels, rgba, size*4);
        for(int k = 0; k < size*4; k+=4) {
            int rgb[3] = { ditheredPixels[k+0], ditheredPixels[k+1], ditheredPixels[k+2] };
            int bestd = 0x7FFFFFFF, best = -1;
            // TODO: exhaustive search. do something better.
            for(int i = 0; i < gif->numColors; ++i) {
                int bb = palette[i*3+0]-rgb[0];
                int gg = palette[i*3+1]-rgb[1];
                int rr = palette[i*3+2]-rgb[2];
                int d = bb*bb + gg*gg + rr*rr;
                if(d < bestd) {
                    bestd = d;
                    best = i;
                }
            }
            indexedPixels[k/4] = best;
            int diff[3] = { ditheredPixels[k+0] - palette[indexedPixels[k/4]*3+0], ditheredPixels[k+1] - palette[indexedPixels[k/4]*3+1], ditheredPixels[k+2] - palette[indexedPixels[k/4]*3+2] };
            // Floyd-Steinberg Error Diffusion
            // TODO: Use something better -- http://caca.zoy.org/study/part3.html
            if(k+4 < size*4) {
                ditheredPixels[k+4+0] = (unsigned char)jo_gif_clamp(ditheredPixels[k+4+0]+(diff[0]*7/16), 0, 255);
                ditheredPixels[k+4+1] = (unsigned char)jo_gif_clamp(ditheredPixels[k+4+1]+(diff[1]*7/16), 0, 255);
                ditheredPixels[k+4+2] = (unsigned char)jo_gif_clamp(ditheredPixels[k+4+2]+(diff[2]*7/16), 0, 255);
            }
            if(k+width*4+4 < size*4) {
                for(int i = 0; i < 3; ++i) {
                    ditheredPixels[k-4+width*4+i] = (unsigned char)jo_gif_clamp(ditheredPixels[k-4+width*4+i]+(diff[i]*3/16), 0, 255);
                    ditheredPixels[k+width*4+i] = (unsigned char)jo_gif_clamp(ditheredPixels[k+width*4+i]+(diff[i]*5/16), 0, 255);
                    ditheredPixels[k+width*4+4+i] = (unsigned char)jo_gif_clamp(ditheredPixels[k+width*4+4+i]+(diff[i]*1/16), 0, 255);
                }
            }
        }
        free(ditheredPixels);
    }
    if(gif->frame == 0) {
        // Global Color Table
        fwrite(palette, 3*(1<<(gif->palSize+1)), 1, gif->fp);
        if(gif->repeat >= 0) {
            // Netscape Extension
            fwrite("\x21\xff\x0bNETSCAPE2.0\x03\x01", 16, 1, gif->fp);
            fwrite(&gif->repeat, 2, 1, gif->fp); // loop count (extra iterations, 0=repeat forever)
            putc(0, gif->fp); // block terminator
        }
    }
    // Graphic Control Extension
    fwrite("\x21\xf9\x04\x00", 4, 1, gif->fp);
    fwrite(&delayCsec, 2, 1, gif->fp); // delayCsec x 1/100 sec
    fwrite("\x00\x00", 2, 1, gif->fp); // transparent color index (first byte), currently unused
    // Image Descriptor
    fwrite("\x2c\x00\x00\x00\x00", 5, 1, gif->fp); // header, x,y
    fwrite(&width, 2, 1, gif->fp);
    fwrite(&height, 2, 1, gif->fp);
    if (gif->frame == 0 || !localPalette) {
        putc(0, gif->fp);
    } else {
        putc(0x80|gif->palSize, gif->fp );
        fwrite(palette, 3*(1<<(gif->palSize+1)), 1, gif->fp);
    }
    putc(8, gif->fp); // block terminator
    jo_gif_lzw_encode(indexedPixels, size, gif->fp);
    putc(0, gif->fp); // block terminator
    ++gif->frame;
    free(indexedPixels);
}

inline void jo_gif_end(jo_gif_t *gif) {
    if(!gif->fp) {
        return;
    }
    putc(0x3b, gif->fp); // gif trailer
    fclose(gif->fp);
}

#endif /*JO_INCLUDE_GIF_H*/
#endif /*CTURTLE_HEADLESS*/

//MIT License
//
//Copyright (c) 2019 Jesse W. Walker
//
//Permission is hereby granted, free of charge, to any person obtaining a copy
//of this software and associated documentation files (the "Software"), to deal
//in the Software without restriction, including without limitation the rights
//to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//copies of the Software, and to permit persons to whom the Software is
//furnished to do so, subject to the following conditions:
//
//The above copyright notice and this permission notice shall be included in all
//copies or substantial portions of the Software.
//
//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//SOFTWARE.

/*
 * File:    CTurtle.hpp
 * Project: C-Turtle
 * Created on September 18, 2019, 10:44 AM
 */

#pragma once

//Automatic linking when operating under MSVC
//If linking errors occur when compiling on Non-MSVC,
//Make sure you link X11 and PThread when using Unix-Like environments, when NOT using headless mode.
#ifndef CTURTLE_MSVC_NO_AUTOLINK
#ifdef _MSC_VER
/*Automatically link to the necessary windows libraries while under MSVC.*/
#pragma comment(lib, "kernel32.lib")
#pragma comment(lib, "gdi32.lib")
#endif
#endif

//MSVC 2017 doesn't seem to like defining M_PI. We define it ourselves
//when compiling under VisualC++.
#ifndef _MSC_VER
#include <cmath>//for M_PI
#else
#ifndef M_PI
#define M_PI 3.14159265358979323846264338327950288
#endif
#endif

//When using headless, simply pre-define CTURTLE_CONFIG_HEADLESS.
//This disables the InteractiveTurtleScreen.
//GIF utility is included at the top of the file when under headless mode.

#ifdef CTURTLE_HEADLESS
    //Optional define to disable HTML Base64 Image output
    //#define CTURTLE_HEADLESS_NO_HTML

    //Disable CImg Display
    #define cimg_display 0

    //Define default width and height.
    #ifndef CTURTLE_HEADLESS_WIDTH
        #define CTURTLE_HEADLESS_WIDTH 400
    #endif

    #ifndef CTURTLE_HEADLESS_HEIGHT
        #define CTURTLE_HEADLESS_HEIGHT 300
    #endif

    #ifndef CTURTLE_HEADLESS_SAVEDIR
        #define CTURTLE_HEADLESS_SAVEDIR "./cturtle.gif"
    #endif
#endif

#ifdef _MSC_VER
//Disable MSVC warnings for CImg. Irrelevant to project.
#include <CodeAnalysis/Warnings.h>
#pragma warning(push, 0)
#pragma warning (disable : ALL_CODE_ANALYSIS_WARNINGS)
#include "CImg.h"
#pragma warning(pop)
#else
#include "CImg.h"
#endif

//For specific integer types, maps, strings, etc.
#include <unordered_map>
#include <string>
#include <cstdint>
#include <fstream>
#include <vector>

//Used for random number generation.
#include <chrono>
#include <random>

#include <memory>       //For smart pointers.
#include <mutex>        //Mutex object for event thread synchronization.

#include <list>
#include <functional>

#include <tuple>    //Used for CompoundShapes
#include <cstring>  //memcpy
#include <vector>   //For Polygon point storage
#include <cmath>    //For rounding, etc
#include <array>    //For Transform storage.

#include <thread>
#include <fstream>
#include <iostream>
#include <sstream>//used for base64 encoding.

//See https://github.com/mvorbrodt/blog/blob/master/src/base64.hpp for original source.
//The below has been modified to use unsigned characters to avoid signed->unsigned->signed fiddling.
namespace base64{
    static constexpr unsigned char kEncodeLookup[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    static constexpr unsigned char kPadCharacter = '=';

    /**
     * Encodes a given unsigned character buffer to Base64.
     * Can be a file, for example.
     * @param input data buffer
     * @return Base64 encoded string.
     */
    inline std::string encode(const std::vector<unsigned char>& input)
    {
        std::stringstream encoded;
        std::uint32_t temp{};

        auto it = input.begin();

        for(std::size_t i = 0; i < input.size() / 3; ++i)
        {
            temp  = (*it++) << 16;
            temp += (*it++) << 8;
            temp += (*it++);
            encoded << kEncodeLookup[(temp & 0x00FC0000) >> 18];
            encoded << kEncodeLookup[(temp & 0x0003F000) >> 12];
            encoded << kEncodeLookup[(temp & 0x00000FC0) >> 6 ];
            encoded << kEncodeLookup[(temp & 0x0000003F)      ];
        }

        switch(input.size() % 3)
        {
            case 1:
                temp = (*it++) << 16;
                encoded << kEncodeLookup[(temp & 0x00FC0000) >> 18];
                encoded << kEncodeLookup[(temp & 0x0003F000) >> 12];
                encoded << kPadCharacter << kPadCharacter;
                break;
            case 2:
                temp  = (*it++) << 16;
                temp += (*it++) << 8;
                encoded << kEncodeLookup[(temp & 0x00FC0000) >> 18];
                encoded << kEncodeLookup[(temp & 0x0003F000) >> 12];
                encoded << kEncodeLookup[(temp & 0x00000FC0) >> 6 ];
                encoded << kPadCharacter;
                break;
        }

        return encoded.str();
    }
}

namespace cturtle {
    /**The CImg library namespace alias used by the CTurtle library.*/
    namespace cimg = cimg_library;
    /**The common Image type used by CTurtle.*/
    typedef cimg::CImg<uint8_t> Image;

    namespace detail {
        // SECTION: COLORS
        // In an effort to make this package easily distributable,
        // Colors are defined as packed integers in the header file.
        //===========================
        typedef uint32_t color_int_t; //Alpha value is extra, serves as padding
        typedef uint64_t time_t;

        /**
         * Pack three bytes into an integer to represent a color at compile time.
         * @param r
         * @param g
         * @param b
         * @return
         */
        inline constexpr color_int_t resolveColorInt(uint8_t r, uint8_t g, uint8_t b) {
            return ((r & 0xFF) << 16) + ((g & 0xFF) << 8) + (b & 0xFF);
        }

        /**
         * Unpacks R, G, and B bytes to the specified pointer (assumes sequential components).
         * @param pack
         * @param colorPtr
         */
        inline void resolveColorComp(color_int_t pack, uint8_t& r, uint8_t& g, uint8_t& b) {
            r = (pack & 0x00FF0000) >> 16; //Red
            g = (pack & 0x0000FF00) >> 8; //Green
            b = (pack & 0x000000FF); // >> 0;  //Blue
        }

        /**
         * Returns the total number of milliseconds elapsed since the UNIX epoch.
         * @return
         */
        inline time_t epochTime() {
            return std::chrono::system_clock::now().time_since_epoch() / std::chrono::milliseconds(1);
        }

        /**\brief Sleeps the calling thread the specified amount of milliseconds.
         *\param ms The total number of milliseconds to sleep.*/
        inline void sleep(long ms) {
            if (ms <= 0)
                return;
            std::this_thread::sleep_for(std::chrono::milliseconds(ms));
        }

        namespace col {
            const detail::color_int_t alice_blue = detail::resolveColorInt(240, 248, 255);
            const detail::color_int_t AliceBlue = detail::resolveColorInt(240, 248, 255);
            const detail::color_int_t antique_white = detail::resolveColorInt(250, 235, 215);
            const detail::color_int_t AntiqueWhite = detail::resolveColorInt(250, 235, 215);
            const detail::color_int_t AntiqueWhite1 = detail::resolveColorInt(255, 239, 219);
            const detail::color_int_t AntiqueWhite2 = detail::resolveColorInt(238, 223, 204);
            const detail::color_int_t AntiqueWhite3 = detail::resolveColorInt(205, 192, 176);
            const detail::color_int_t AntiqueWhite4 = detail::resolveColorInt(139, 131, 120);
            const detail::color_int_t aquamarine = detail::resolveColorInt(127, 255, 212);
            const detail::color_int_t aquamarine1 = detail::resolveColorInt(127, 255, 212);
            const detail::color_int_t aquamarine2 = detail::resolveColorInt(118, 238, 198);
            const detail::color_int_t aquamarine3 = detail::resolveColorInt(102, 205, 170);
            const detail::color_int_t aquamarine4 = detail::resolveColorInt(69, 139, 116);
            const detail::color_int_t azure = detail::resolveColorInt(240, 255, 255);
            const detail::color_int_t azure1 = detail::resolveColorInt(240, 255, 255);
            const detail::color_int_t azure2 = detail::resolveColorInt(224, 238, 238);
            const detail::color_int_t azure3 = detail::resolveColorInt(193, 205, 205);
            const detail::color_int_t azure4 = detail::resolveColorInt(131, 139, 139);
            const detail::color_int_t beige = detail::resolveColorInt(245, 245, 220);
            const detail::color_int_t bisque = detail::resolveColorInt(255, 228, 196);
            const detail::color_int_t bisque1 = detail::resolveColorInt(255, 228, 196);
            const detail::color_int_t bisque2 = detail::resolveColorInt(238, 213, 183);
            const detail::color_int_t bisque3 = detail::resolveColorInt(205, 183, 158);
            const detail::color_int_t bisque4 = detail::resolveColorInt(139, 125, 107);
            const detail::color_int_t black = detail::resolveColorInt(0, 0, 0);
            const detail::color_int_t blanched_almond = detail::resolveColorInt(255, 235, 205);
            const detail::color_int_t BlanchedAlmond = detail::resolveColorInt(255, 235, 205);
            const detail::color_int_t blue = detail::resolveColorInt(0, 0, 255);
            const detail::color_int_t blue_violet = detail::resolveColorInt(138, 43, 226);
            const detail::color_int_t blue1 = detail::resolveColorInt(0, 0, 255);
            const detail::color_int_t blue2 = detail::resolveColorInt(0, 0, 238);
            const detail::color_int_t blue3 = detail::resolveColorInt(0, 0, 205);
            const detail::color_int_t blue4 = detail::resolveColorInt(0, 0, 139);
            const detail::color_int_t BlueViolet = detail::resolveColorInt(138, 43, 226);
            const detail::color_int_t brown = detail::resolveColorInt(165, 42, 42);
            const detail::color_int_t brown1 = detail::resolveColorInt(255, 64, 64);
            const detail::color_int_t brown2 = detail::resolveColorInt(238, 59, 59);
            const detail::color_int_t brown3 = detail::resolveColorInt(205, 51, 51);
            const detail::color_int_t brown4 = detail::resolveColorInt(139, 35, 35);
            const detail::color_int_t burlywood = detail::resolveColorInt(222, 184, 135);
            const detail::color_int_t burlywood1 = detail::resolveColorInt(255, 211, 155);
            const detail::color_int_t burlywood2 = detail::resolveColorInt(238, 197, 145);
            const detail::color_int_t burlywood3 = detail::resolveColorInt(205, 170, 125);
            const detail::color_int_t burlywood4 = detail::resolveColorInt(139, 115, 85);
            const detail::color_int_t cadet_blue = detail::resolveColorInt(95, 158, 160);
            const detail::color_int_t CadetBlue = detail::resolveColorInt(95, 158, 160);
            const detail::color_int_t CadetBlue1 = detail::resolveColorInt(152, 245, 255);
            const detail::color_int_t CadetBlue2 = detail::resolveColorInt(142, 229, 238);
            const detail::color_int_t CadetBlue3 = detail::resolveColorInt(122, 197, 205);
            const detail::color_int_t CadetBlue4 = detail::resolveColorInt(83, 134, 139);
            const detail::color_int_t chartreuse = detail::resolveColorInt(127, 255, 0);
            const detail::color_int_t chartreuse1 = detail::resolveColorInt(127, 255, 0);
            const detail::color_int_t chartreuse2 = detail::resolveColorInt(118, 238, 0);
            const detail::color_int_t chartreuse3 = detail::resolveColorInt(102, 205, 0);
            const detail::color_int_t chartreuse4 = detail::resolveColorInt(69, 139, 0);
            const detail::color_int_t chocolate = detail::resolveColorInt(210, 105, 30);
            const detail::color_int_t chocolate1 = detail::resolveColorInt(255, 127, 36);
            const detail::color_int_t chocolate2 = detail::resolveColorInt(238, 118, 33);
            const detail::color_int_t chocolate3 = detail::resolveColorInt(205, 102, 29);
            const detail::color_int_t chocolate4 = detail::resolveColorInt(139, 69, 19);
            const detail::color_int_t coral = detail::resolveColorInt(255, 127, 80);
            const detail::color_int_t coral1 = detail::resolveColorInt(255, 114, 86);
            const detail::color_int_t coral2 = detail::resolveColorInt(238, 106, 80);
            const detail::color_int_t coral3 = detail::resolveColorInt(205, 91, 69);
            const detail::color_int_t coral4 = detail::resolveColorInt(139, 62, 47);
            const detail::color_int_t cornflower_blue = detail::resolveColorInt(100, 149, 237);
            const detail::color_int_t CornflowerBlue = detail::resolveColorInt(100, 149, 237);
            const detail::color_int_t cornsilk = detail::resolveColorInt(255, 248, 220);
            const detail::color_int_t cornsilk1 = detail::resolveColorInt(255, 248, 220);
            const detail::color_int_t cornsilk2 = detail::resolveColorInt(238, 232, 205);
            const detail::color_int_t cornsilk3 = detail::resolveColorInt(205, 200, 177);
            const detail::color_int_t cornsilk4 = detail::resolveColorInt(139, 136, 120);
            const detail::color_int_t cyan = detail::resolveColorInt(0, 255, 255);
            const detail::color_int_t cyan1 = detail::resolveColorInt(0, 255, 255);
            const detail::color_int_t cyan2 = detail::resolveColorInt(0, 238, 238);
            const detail::color_int_t cyan3 = detail::resolveColorInt(0, 205, 205);
            const detail::color_int_t cyan4 = detail::resolveColorInt(0, 139, 139);
            const detail::color_int_t dark_blue = detail::resolveColorInt(0, 0, 139);
            const detail::color_int_t dark_cyan = detail::resolveColorInt(0, 139, 139);
            const detail::color_int_t dark_goldenrod = detail::resolveColorInt(184, 134, 11);
            const detail::color_int_t dark_gray = detail::resolveColorInt(169, 169, 169);
            const detail::color_int_t dark_green = detail::resolveColorInt(0, 100, 0);
            const detail::color_int_t dark_grey = detail::resolveColorInt(169, 169, 169);
            const detail::color_int_t dark_khaki = detail::resolveColorInt(189, 183, 107);
            const detail::color_int_t dark_magenta = detail::resolveColorInt(139, 0, 139);
            const detail::color_int_t dark_olive_green = detail::resolveColorInt(85, 107, 47);
            const detail::color_int_t dark_orange = detail::resolveColorInt(255, 140, 0);
            const detail::color_int_t dark_orchid = detail::resolveColorInt(153, 50, 204);
            const detail::color_int_t dark_red = detail::resolveColorInt(139, 0, 0);
            const detail::color_int_t dark_salmon = detail::resolveColorInt(233, 150, 122);
            const detail::color_int_t dark_sea_green = detail::resolveColorInt(143, 188, 143);
            const detail::color_int_t dark_slate_blue = detail::resolveColorInt(72, 61, 139);
            const detail::color_int_t dark_slate_gray = detail::resolveColorInt(47, 79, 79);
            const detail::color_int_t dark_slate_grey = detail::resolveColorInt(47, 79, 79);
            const detail::color_int_t dark_turquoise = detail::resolveColorInt(0, 206, 209);
            const detail::color_int_t dark_violet = detail::resolveColorInt(148, 0, 211);
            const detail::color_int_t DarkBlue = detail::resolveColorInt(0, 0, 139);
            const detail::color_int_t DarkCyan = detail::resolveColorInt(0, 139, 139);
            const detail::color_int_t DarkGoldenrod = detail::resolveColorInt(184, 134, 11);
            const detail::color_int_t DarkGoldenrod1 = detail::resolveColorInt(255, 185, 15);
            const detail::color_int_t DarkGoldenrod2 = detail::resolveColorInt(238, 173, 14);
            const detail::color_int_t DarkGoldenrod3 = detail::resolveColorInt(205, 149, 12);
            const detail::color_int_t DarkGoldenrod4 = detail::resolveColorInt(139, 101, 8);
            const detail::color_int_t DarkGray = detail::resolveColorInt(169, 169, 169);
            const detail::color_int_t DarkGreen = detail::resolveColorInt(0, 100, 0);
            const detail::color_int_t DarkGrey = detail::resolveColorInt(169, 169, 169);
            const detail::color_int_t DarkKhaki = detail::resolveColorInt(189, 183, 107);
            const detail::color_int_t DarkMagenta = detail::resolveColorInt(139, 0, 139);
            const detail::color_int_t DarkOliveGreen = detail::resolveColorInt(85, 107, 47);
            const detail::color_int_t DarkOliveGreen1 = detail::resolveColorInt(202, 255, 112);
            const detail::color_int_t DarkOliveGreen2 = detail::resolveColorInt(188, 238, 104);
            const detail::color_int_t DarkOliveGreen3 = detail::resolveColorInt(162, 205, 90);
            const detail::color_int_t DarkOliveGreen4 = detail::resolveColorInt(110, 139, 61);
            const detail::color_int_t DarkOrange = detail::resolveColorInt(255, 140, 0);
            const detail::color_int_t DarkOrange1 = detail::resolveColorInt(255, 127, 0);
            const detail::color_int_t DarkOrange2 = detail::resolveColorInt(238, 118, 0);
            const detail::color_int_t DarkOrange3 = detail::resolveColorInt(205, 102, 0);
            const detail::color_int_t DarkOrange4 = detail::resolveColorInt(139, 69, 0);
            const detail::color_int_t DarkOrchid = detail::resolveColorInt(153, 50, 204);
            const detail::color_int_t DarkOrchid1 = detail::resolveColorInt(191, 62, 255);
            const detail::color_int_t DarkOrchid2 = detail::resolveColorInt(178, 58, 238);
            const detail::color_int_t DarkOrchid3 = detail::resolveColorInt(154, 50, 205);
            const detail::color_int_t DarkOrchid4 = detail::resolveColorInt(104, 34, 139);
            const detail::color_int_t DarkRed = detail::resolveColorInt(139, 0, 0);
            const detail::color_int_t DarkSalmon = detail::resolveColorInt(233, 150, 122);
            const detail::color_int_t DarkSeaGreen = detail::resolveColorInt(143, 188, 143);
            const detail::color_int_t DarkSeaGreen1 = detail::resolveColorInt(193, 255, 193);
            const detail::color_int_t DarkSeaGreen2 = detail::resolveColorInt(180, 238, 180);
            const detail::color_int_t DarkSeaGreen3 = detail::resolveColorInt(155, 205, 155);
            const detail::color_int_t DarkSeaGreen4 = detail::resolveColorInt(105, 139, 105);
            const detail::color_int_t DarkSlateBlue = detail::resolveColorInt(72, 61, 139);
            const detail::color_int_t DarkSlateGray = detail::resolveColorInt(47, 79, 79);
            const detail::color_int_t DarkSlateGray1 = detail::resolveColorInt(151, 255, 255);
            const detail::color_int_t DarkSlateGray2 = detail::resolveColorInt(141, 238, 238);
            const detail::color_int_t DarkSlateGray3 = detail::resolveColorInt(121, 205, 205);
            const detail::color_int_t DarkSlateGray4 = detail::resolveColorInt(82, 139, 139);
            const detail::color_int_t DarkSlateGrey = detail::resolveColorInt(47, 79, 79);
            const detail::color_int_t DarkTurquoise = detail::resolveColorInt(0, 206, 209);
            const detail::color_int_t DarkViolet = detail::resolveColorInt(148, 0, 211);
            const detail::color_int_t deep_pink = detail::resolveColorInt(255, 20, 147);
            const detail::color_int_t deep_sky_blue = detail::resolveColorInt(0, 191, 255);
            const detail::color_int_t DeepPink = detail::resolveColorInt(255, 20, 147);
            const detail::color_int_t DeepPink1 = detail::resolveColorInt(255, 20, 147);
            const detail::color_int_t DeepPink2 = detail::resolveColorInt(238, 18, 137);
            const detail::color_int_t DeepPink3 = detail::resolveColorInt(205, 16, 118);
            const detail::color_int_t DeepPink4 = detail::resolveColorInt(139, 10, 80);
            const detail::color_int_t DeepSkyBlue = detail::resolveColorInt(0, 191, 255);
            const detail::color_int_t DeepSkyBlue1 = detail::resolveColorInt(0, 191, 255);
            const detail::color_int_t DeepSkyBlue2 = detail::resolveColorInt(0, 178, 238);
            const detail::color_int_t DeepSkyBlue3 = detail::resolveColorInt(0, 154, 205);
            const detail::color_int_t DeepSkyBlue4 = detail::resolveColorInt(0, 104, 139);
            const detail::color_int_t dim_gray = detail::resolveColorInt(105, 105, 105);
            const detail::color_int_t dim_grey = detail::resolveColorInt(105, 105, 105);
            const detail::color_int_t DimGray = detail::resolveColorInt(105, 105, 105);
            const detail::color_int_t DimGrey = detail::resolveColorInt(105, 105, 105);
            const detail::color_int_t dodger_blue = detail::resolveColorInt(30, 144, 255);
            const detail::color_int_t DodgerBlue = detail::resolveColorInt(30, 144, 255);
            const detail::color_int_t DodgerBlue1 = detail::resolveColorInt(30, 144, 255);
            const detail::color_int_t DodgerBlue2 = detail::resolveColorInt(28, 134, 238);
            const detail::color_int_t DodgerBlue3 = detail::resolveColorInt(24, 116, 205);
            const detail::color_int_t DodgerBlue4 = detail::resolveColorInt(16, 78, 139);
            const detail::color_int_t firebrick = detail::resolveColorInt(178, 34, 34);
            const detail::color_int_t firebrick1 = detail::resolveColorInt(255, 48, 48);
            const detail::color_int_t firebrick2 = detail::resolveColorInt(238, 44, 44);
            const detail::color_int_t firebrick3 = detail::resolveColorInt(205, 38, 38);
            const detail::color_int_t firebrick4 = detail::resolveColorInt(139, 26, 26);
            const detail::color_int_t floral_white = detail::resolveColorInt(255, 250, 240);
            const detail::color_int_t FloralWhite = detail::resolveColorInt(255, 250, 240);
            const detail::color_int_t forest_green = detail::resolveColorInt(34, 139, 34);
            const detail::color_int_t ForestGreen = detail::resolveColorInt(34, 139, 34);
            const detail::color_int_t gainsboro = detail::resolveColorInt(220, 220, 220);
            const detail::color_int_t ghost_white = detail::resolveColorInt(248, 248, 255);
            const detail::color_int_t GhostWhite = detail::resolveColorInt(248, 248, 255);
            const detail::color_int_t gold = detail::resolveColorInt(255, 215, 0);
            const detail::color_int_t gold1 = detail::resolveColorInt(255, 215, 0);
            const detail::color_int_t gold2 = detail::resolveColorInt(238, 201, 0);
            const detail::color_int_t gold3 = detail::resolveColorInt(205, 173, 0);
            const detail::color_int_t gold4 = detail::resolveColorInt(139, 117, 0);
            const detail::color_int_t goldenrod = detail::resolveColorInt(218, 165, 32);
            const detail::color_int_t goldenrod1 = detail::resolveColorInt(255, 193, 37);
            const detail::color_int_t goldenrod2 = detail::resolveColorInt(238, 180, 34);
            const detail::color_int_t goldenrod3 = detail::resolveColorInt(205, 155, 29);
            const detail::color_int_t goldenrod4 = detail::resolveColorInt(139, 105, 20);
            const detail::color_int_t gray = detail::resolveColorInt(190, 190, 190);
            const detail::color_int_t gray0 = detail::resolveColorInt(0, 0, 0);
            const detail::color_int_t gray1 = detail::resolveColorInt(3, 3, 3);
            const detail::color_int_t gray2 = detail::resolveColorInt(5, 5, 5);
            const detail::color_int_t gray3 = detail::resolveColorInt(8, 8, 8);
            const detail::color_int_t gray4 = detail::resolveColorInt(10, 10, 10);
            const detail::color_int_t gray5 = detail::resolveColorInt(13, 13, 13);
            const detail::color_int_t gray6 = detail::resolveColorInt(15, 15, 15);
            const detail::color_int_t gray7 = detail::resolveColorInt(18, 18, 18);
            const detail::color_int_t gray8 = detail::resolveColorInt(20, 20, 20);
            const detail::color_int_t gray9 = detail::resolveColorInt(23, 23, 23);
            const detail::color_int_t gray10 = detail::resolveColorInt(26, 26, 26);
            const detail::color_int_t gray11 = detail::resolveColorInt(28, 28, 28);
            const detail::color_int_t gray12 = detail::resolveColorInt(31, 31, 31);
            const detail::color_int_t gray13 = detail::resolveColorInt(33, 33, 33);
            const detail::color_int_t gray14 = detail::resolveColorInt(36, 36, 36);
            const detail::color_int_t gray15 = detail::resolveColorInt(38, 38, 38);
            const detail::color_int_t gray16 = detail::resolveColorInt(41, 41, 41);
            const detail::color_int_t gray17 = detail::resolveColorInt(43, 43, 43);
            const detail::color_int_t gray18 = detail::resolveColorInt(46, 46, 46);
            const detail::color_int_t gray19 = detail::resolveColorInt(48, 48, 48);
            const detail::color_int_t gray20 = detail::resolveColorInt(51, 51, 51);
            const detail::color_int_t gray21 = detail::resolveColorInt(54, 54, 54);
            const detail::color_int_t gray22 = detail::resolveColorInt(56, 56, 56);
            const detail::color_int_t gray23 = detail::resolveColorInt(59, 59, 59);
            const detail::color_int_t gray24 = detail::resolveColorInt(61, 61, 61);
            const detail::color_int_t gray25 = detail::resolveColorInt(64, 64, 64);
            const detail::color_int_t gray26 = detail::resolveColorInt(66, 66, 66);
            const detail::color_int_t gray27 = detail::resolveColorInt(69, 69, 69);
            const detail::color_int_t gray28 = detail::resolveColorInt(71, 71, 71);
            const detail::color_int_t gray29 = detail::resolveColorInt(74, 74, 74);
            const detail::color_int_t gray30 = detail::resolveColorInt(77, 77, 77);
            const detail::color_int_t gray31 = detail::resolveColorInt(79, 79, 79);
            const detail::color_int_t gray32 = detail::resolveColorInt(82, 82, 82);
            const detail::color_int_t gray33 = detail::resolveColorInt(84, 84, 84);
            const detail::color_int_t gray34 = detail::resolveColorInt(87, 87, 87);
            const detail::color_int_t gray35 = detail::resolveColorInt(89, 89, 89);
            const detail::color_int_t gray36 = detail::resolveColorInt(92, 92, 92);
            const detail::color_int_t gray37 = detail::resolveColorInt(94, 94, 94);
            const detail::color_int_t gray38 = detail::resolveColorInt(97, 97, 97);
            const detail::color_int_t gray39 = detail::resolveColorInt(99, 99, 99);
            const detail::color_int_t gray40 = detail::resolveColorInt(102, 102, 102);
            const detail::color_int_t gray41 = detail::resolveColorInt(105, 105, 105);
            const detail::color_int_t gray42 = detail::resolveColorInt(107, 107, 107);
            const detail::color_int_t gray43 = detail::resolveColorInt(110, 110, 110);
            const detail::color_int_t gray44 = detail::resolveColorInt(112, 112, 112);
            const detail::color_int_t gray45 = detail::resolveColorInt(115, 115, 115);
            const detail::color_int_t gray46 = detail::resolveColorInt(117, 117, 117);
            const detail::color_int_t gray47 = detail::resolveColorInt(120, 120, 120);
            const detail::color_int_t gray48 = detail::resolveColorInt(122, 122, 122);
            const detail::color_int_t gray49 = detail::resolveColorInt(125, 125, 125);
            const detail::color_int_t gray50 = detail::resolveColorInt(127, 127, 127);
            const detail::color_int_t gray51 = detail::resolveColorInt(130, 130, 130);
            const detail::color_int_t gray52 = detail::resolveColorInt(133, 133, 133);
            const detail::color_int_t gray53 = detail::resolveColorInt(135, 135, 135);
            const detail::color_int_t gray54 = detail::resolveColorInt(138, 138, 138);
            const detail::color_int_t gray55 = detail::resolveColorInt(140, 140, 140);
            const detail::color_int_t gray56 = detail::resolveColorInt(143, 143, 143);
            const detail::color_int_t gray57 = detail::resolveColorInt(145, 145, 145);
            const detail::color_int_t gray58 = detail::resolveColorInt(148, 148, 148);
            const detail::color_int_t gray59 = detail::resolveColorInt(150, 150, 150);
            const detail::color_int_t gray60 = detail::resolveColorInt(153, 153, 153);
            const detail::color_int_t gray61 = detail::resolveColorInt(156, 156, 156);
            const detail::color_int_t gray62 = detail::resolveColorInt(158, 158, 158);
            const detail::color_int_t gray63 = detail::resolveColorInt(161, 161, 161);
            const detail::color_int_t gray64 = detail::resolveColorInt(163, 163, 163);
            const detail::color_int_t gray65 = detail::resolveColorInt(166, 166, 166);
            const detail::color_int_t gray66 = detail::resolveColorInt(168, 168, 168);
            const detail::color_int_t gray67 = detail::resolveColorInt(171, 171, 171);
            const detail::color_int_t gray68 = detail::resolveColorInt(173, 173, 173);
            const detail::color_int_t gray69 = detail::resolveColorInt(176, 176, 176);
            const detail::color_int_t gray70 = detail::resolveColorInt(179, 179, 179);
            const detail::color_int_t gray71 = detail::resolveColorInt(181, 181, 181);
            const detail::color_int_t gray72 = detail::resolveColorInt(184, 184, 184);
            const detail::color_int_t gray73 = detail::resolveColorInt(186, 186, 186);
            const detail::color_int_t gray74 = detail::resolveColorInt(189, 189, 189);
            const detail::color_int_t gray75 = detail::resolveColorInt(191, 191, 191);
            const detail::color_int_t gray76 = detail::resolveColorInt(194, 194, 194);
            const detail::color_int_t gray77 = detail::resolveColorInt(196, 196, 196);
            const detail::color_int_t gray78 = detail::resolveColorInt(199, 199, 199);
            const detail::color_int_t gray79 = detail::resolveColorInt(201, 201, 201);
            const detail::color_int_t gray80 = detail::resolveColorInt(204, 204, 204);
            const detail::color_int_t gray81 = detail::resolveColorInt(207, 207, 207);
            const detail::color_int_t gray82 = detail::resolveColorInt(209, 209, 209);
            const detail::color_int_t gray83 = detail::resolveColorInt(212, 212, 212);
            const detail::color_int_t gray84 = detail::resolveColorInt(214, 214, 214);
            const detail::color_int_t gray85 = detail::resolveColorInt(217, 217, 217);
            const detail::color_int_t gray86 = detail::resolveColorInt(219, 219, 219);
            const detail::color_int_t gray87 = detail::resolveColorInt(222, 222, 222);
            const detail::color_int_t gray88 = detail::resolveColorInt(224, 224, 224);
            const detail::color_int_t gray89 = detail::resolveColorInt(227, 227, 227);
            const detail::color_int_t gray90 = detail::resolveColorInt(229, 229, 229);
            const detail::color_int_t gray91 = detail::resolveColorInt(232, 232, 232);
            const detail::color_int_t gray92 = detail::resolveColorInt(235, 235, 235);
            const detail::color_int_t gray93 = detail::resolveColorInt(237, 237, 237);
            const detail::color_int_t gray94 = detail::resolveColorInt(240, 240, 240);
            const detail::color_int_t gray95 = detail::resolveColorInt(242, 242, 242);
            const detail::color_int_t gray96 = detail::resolveColorInt(245, 245, 245);
            const detail::color_int_t gray97 = detail::resolveColorInt(247, 247, 247);
            const detail::color_int_t gray98 = detail::resolveColorInt(250, 250, 250);
            const detail::color_int_t gray99 = detail::resolveColorInt(252, 252, 252);
            const detail::color_int_t gray100 = detail::resolveColorInt(255, 255, 255);
            const detail::color_int_t green = detail::resolveColorInt(0, 255, 0);
            const detail::color_int_t green_yellow = detail::resolveColorInt(173, 255, 47);
            const detail::color_int_t green1 = detail::resolveColorInt(0, 255, 0);
            const detail::color_int_t green2 = detail::resolveColorInt(0, 238, 0);
            const detail::color_int_t green3 = detail::resolveColorInt(0, 205, 0);
            const detail::color_int_t green4 = detail::resolveColorInt(0, 139, 0);
            const detail::color_int_t GreenYellow = detail::resolveColorInt(173, 255, 47);
            const detail::color_int_t grey = detail::resolveColorInt(190, 190, 190);
            const detail::color_int_t grey0 = detail::resolveColorInt(0, 0, 0);
            const detail::color_int_t grey1 = detail::resolveColorInt(3, 3, 3);
            const detail::color_int_t grey2 = detail::resolveColorInt(5, 5, 5);
            const detail::color_int_t grey3 = detail::resolveColorInt(8, 8, 8);
            const detail::color_int_t grey4 = detail::resolveColorInt(10, 10, 10);
            const detail::color_int_t grey5 = detail::resolveColorInt(13, 13, 13);
            const detail::color_int_t grey6 = detail::resolveColorInt(15, 15, 15);
            const detail::color_int_t grey7 = detail::resolveColorInt(18, 18, 18);
            const detail::color_int_t grey8 = detail::resolveColorInt(20, 20, 20);
            const detail::color_int_t grey9 = detail::resolveColorInt(23, 23, 23);
            const detail::color_int_t grey10 = detail::resolveColorInt(26, 26, 26);
            const detail::color_int_t grey11 = detail::resolveColorInt(28, 28, 28);
            const detail::color_int_t grey12 = detail::resolveColorInt(31, 31, 31);
            const detail::color_int_t grey13 = detail::resolveColorInt(33, 33, 33);
            const detail::color_int_t grey14 = detail::resolveColorInt(36, 36, 36);
            const detail::color_int_t grey15 = detail::resolveColorInt(38, 38, 38);
            const detail::color_int_t grey16 = detail::resolveColorInt(41, 41, 41);
            const detail::color_int_t grey17 = detail::resolveColorInt(43, 43, 43);
            const detail::color_int_t grey18 = detail::resolveColorInt(46, 46, 46);
            const detail::color_int_t grey19 = detail::resolveColorInt(48, 48, 48);
            const detail::color_int_t grey20 = detail::resolveColorInt(51, 51, 51);
            const detail::color_int_t grey21 = detail::resolveColorInt(54, 54, 54);
            const detail::color_int_t grey22 = detail::resolveColorInt(56, 56, 56);
            const detail::color_int_t grey23 = detail::resolveColorInt(59, 59, 59);
            const detail::color_int_t grey24 = detail::resolveColorInt(61, 61, 61);
            const detail::color_int_t grey25 = detail::resolveColorInt(64, 64, 64);
            const detail::color_int_t grey26 = detail::resolveColorInt(66, 66, 66);
            const detail::color_int_t grey27 = detail::resolveColorInt(69, 69, 69);
            const detail::color_int_t grey28 = detail::resolveColorInt(71, 71, 71);
            const detail::color_int_t grey29 = detail::resolveColorInt(74, 74, 74);
            const detail::color_int_t grey30 = detail::resolveColorInt(77, 77, 77);
            const detail::color_int_t grey31 = detail::resolveColorInt(79, 79, 79);
            const detail::color_int_t grey32 = detail::resolveColorInt(82, 82, 82);
            const detail::color_int_t grey33 = detail::resolveColorInt(84, 84, 84);
            const detail::color_int_t grey34 = detail::resolveColorInt(87, 87, 87);
            const detail::color_int_t grey35 = detail::resolveColorInt(89, 89, 89);
            const detail::color_int_t grey36 = detail::resolveColorInt(92, 92, 92);
            const detail::color_int_t grey37 = detail::resolveColorInt(94, 94, 94);
            const detail::color_int_t grey38 = detail::resolveColorInt(97, 97, 97);
            const detail::color_int_t grey39 = detail::resolveColorInt(99, 99, 99);
            const detail::color_int_t grey40 = detail::resolveColorInt(102, 102, 102);
            const detail::color_int_t grey41 = detail::resolveColorInt(105, 105, 105);
            const detail::color_int_t grey42 = detail::resolveColorInt(107, 107, 107);
            const detail::color_int_t grey43 = detail::resolveColorInt(110, 110, 110);
            const detail::color_int_t grey44 = detail::resolveColorInt(112, 112, 112);
            const detail::color_int_t grey45 = detail::resolveColorInt(115, 115, 115);
            const detail::color_int_t grey46 = detail::resolveColorInt(117, 117, 117);
            const detail::color_int_t grey47 = detail::resolveColorInt(120, 120, 120);
            const detail::color_int_t grey48 = detail::resolveColorInt(122, 122, 122);
            const detail::color_int_t grey49 = detail::resolveColorInt(125, 125, 125);
            const detail::color_int_t grey50 = detail::resolveColorInt(127, 127, 127);
            const detail::color_int_t grey51 = detail::resolveColorInt(130, 130, 130);
            const detail::color_int_t grey52 = detail::resolveColorInt(133, 133, 133);
            const detail::color_int_t grey53 = detail::resolveColorInt(135, 135, 135);
            const detail::color_int_t grey54 = detail::resolveColorInt(138, 138, 138);
            const detail::color_int_t grey55 = detail::resolveColorInt(140, 140, 140);
            const detail::color_int_t grey56 = detail::resolveColorInt(143, 143, 143);
            const detail::color_int_t grey57 = detail::resolveColorInt(145, 145, 145);
            const detail::color_int_t grey58 = detail::resolveColorInt(148, 148, 148);
            const detail::color_int_t grey59 = detail::resolveColorInt(150, 150, 150);
            const detail::color_int_t grey60 = detail::resolveColorInt(153, 153, 153);
            const detail::color_int_t grey61 = detail::resolveColorInt(156, 156, 156);
            const detail::color_int_t grey62 = detail::resolveColorInt(158, 158, 158);
            const detail::color_int_t grey63 = detail::resolveColorInt(161, 161, 161);
            const detail::color_int_t grey64 = detail::resolveColorInt(163, 163, 163);
            const detail::color_int_t grey65 = detail::resolveColorInt(166, 166, 166);
            const detail::color_int_t grey66 = detail::resolveColorInt(168, 168, 168);
            const detail::color_int_t grey67 = detail::resolveColorInt(171, 171, 171);
            const detail::color_int_t grey68 = detail::resolveColorInt(173, 173, 173);
            const detail::color_int_t grey69 = detail::resolveColorInt(176, 176, 176);
            const detail::color_int_t grey70 = detail::resolveColorInt(179, 179, 179);
            const detail::color_int_t grey71 = detail::resolveColorInt(181, 181, 181);
            const detail::color_int_t grey72 = detail::resolveColorInt(184, 184, 184);
            const detail::color_int_t grey73 = detail::resolveColorInt(186, 186, 186);
            const detail::color_int_t grey74 = detail::resolveColorInt(189, 189, 189);
            const detail::color_int_t grey75 = detail::resolveColorInt(191, 191, 191);
            const detail::color_int_t grey76 = detail::resolveColorInt(194, 194, 194);
            const detail::color_int_t grey77 = detail::resolveColorInt(196, 196, 196);
            const detail::color_int_t grey78 = detail::resolveColorInt(199, 199, 199);
            const detail::color_int_t grey79 = detail::resolveColorInt(201, 201, 201);
            const detail::color_int_t grey80 = detail::resolveColorInt(204, 204, 204);
            const detail::color_int_t grey81 = detail::resolveColorInt(207, 207, 207);
            const detail::color_int_t grey82 = detail::resolveColorInt(209, 209, 209);
            const detail::color_int_t grey83 = detail::resolveColorInt(212, 212, 212);
            const detail::color_int_t grey84 = detail::resolveColorInt(214, 214, 214);
            const detail::color_int_t grey85 = detail::resolveColorInt(217, 217, 217);
            const detail::color_int_t grey86 = detail::resolveColorInt(219, 219, 219);
            const detail::color_int_t grey87 = detail::resolveColorInt(222, 222, 222);
            const detail::color_int_t grey88 = detail::resolveColorInt(224, 224, 224);
            const detail::color_int_t grey89 = detail::resolveColorInt(227, 227, 227);
            const detail::color_int_t grey90 = detail::resolveColorInt(229, 229, 229);
            const detail::color_int_t grey91 = detail::resolveColorInt(232, 232, 232);
            const detail::color_int_t grey92 = detail::resolveColorInt(235, 235, 235);
            const detail::color_int_t grey93 = detail::resolveColorInt(237, 237, 237);
            const detail::color_int_t grey94 = detail::resolveColorInt(240, 240, 240);
            const detail::color_int_t grey95 = detail::resolveColorInt(242, 242, 242);
            const detail::color_int_t grey96 = detail::resolveColorInt(245, 245, 245);
            const detail::color_int_t grey97 = detail::resolveColorInt(247, 247, 247);
            const detail::color_int_t grey98 = detail::resolveColorInt(250, 250, 250);
            const detail::color_int_t grey99 = detail::resolveColorInt(252, 252, 252);
            const detail::color_int_t grey100 = detail::resolveColorInt(255, 255, 255);
            const detail::color_int_t honeydew = detail::resolveColorInt(240, 255, 240);
            const detail::color_int_t honeydew1 = detail::resolveColorInt(240, 255, 240);
            const detail::color_int_t honeydew2 = detail::resolveColorInt(224, 238, 224);
            const detail::color_int_t honeydew3 = detail::resolveColorInt(193, 205, 193);
            const detail::color_int_t honeydew4 = detail::resolveColorInt(131, 139, 131);
            const detail::color_int_t hot_pink = detail::resolveColorInt(255, 105, 180);
            const detail::color_int_t HotPink = detail::resolveColorInt(255, 105, 180);
            const detail::color_int_t HotPink1 = detail::resolveColorInt(255, 110, 180);
            const detail::color_int_t HotPink2 = detail::resolveColorInt(238, 106, 167);
            const detail::color_int_t HotPink3 = detail::resolveColorInt(205, 96, 144);
            const detail::color_int_t HotPink4 = detail::resolveColorInt(139, 58, 98);
            const detail::color_int_t indian_red = detail::resolveColorInt(205, 92, 92);
            const detail::color_int_t IndianRed = detail::resolveColorInt(205, 92, 92);
            const detail::color_int_t IndianRed1 = detail::resolveColorInt(255, 106, 106);
            const detail::color_int_t IndianRed2 = detail::resolveColorInt(238, 99, 99);
            const detail::color_int_t IndianRed3 = detail::resolveColorInt(205, 85, 85);
            const detail::color_int_t IndianRed4 = detail::resolveColorInt(139, 58, 58);
            const detail::color_int_t ivory = detail::resolveColorInt(255, 255, 240);
            const detail::color_int_t ivory1 = detail::resolveColorInt(255, 255, 240);
            const detail::color_int_t ivory2 = detail::resolveColorInt(238, 238, 224);
            const detail::color_int_t ivory3 = detail::resolveColorInt(205, 205, 193);
            const detail::color_int_t ivory4 = detail::resolveColorInt(139, 139, 131);
            const detail::color_int_t khaki = detail::resolveColorInt(240, 230, 140);
            const detail::color_int_t khaki1 = detail::resolveColorInt(255, 246, 143);
            const detail::color_int_t khaki2 = detail::resolveColorInt(238, 230, 133);
            const detail::color_int_t khaki3 = detail::resolveColorInt(205, 198, 115);
            const detail::color_int_t khaki4 = detail::resolveColorInt(139, 134, 78);
            const detail::color_int_t lavender = detail::resolveColorInt(230, 230, 250);
            const detail::color_int_t lavender_blush = detail::resolveColorInt(255, 240, 245);
            const detail::color_int_t LavenderBlush = detail::resolveColorInt(255, 240, 245);
            const detail::color_int_t LavenderBlush1 = detail::resolveColorInt(255, 240, 245);
            const detail::color_int_t LavenderBlush2 = detail::resolveColorInt(238, 224, 229);
            const detail::color_int_t LavenderBlush3 = detail::resolveColorInt(205, 193, 197);
            const detail::color_int_t LavenderBlush4 = detail::resolveColorInt(139, 131, 134);
            const detail::color_int_t lawn_green = detail::resolveColorInt(124, 252, 0);
            const detail::color_int_t LawnGreen = detail::resolveColorInt(124, 252, 0);
            const detail::color_int_t lemon_chiffon = detail::resolveColorInt(255, 250, 205);
            const detail::color_int_t LemonChiffon = detail::resolveColorInt(255, 250, 205);
            const detail::color_int_t LemonChiffon1 = detail::resolveColorInt(255, 250, 205);
            const detail::color_int_t LemonChiffon2 = detail::resolveColorInt(238, 233, 191);
            const detail::color_int_t LemonChiffon3 = detail::resolveColorInt(205, 201, 165);
            const detail::color_int_t LemonChiffon4 = detail::resolveColorInt(139, 137, 112);
            const detail::color_int_t light_blue = detail::resolveColorInt(173, 216, 230);
            const detail::color_int_t light_coral = detail::resolveColorInt(240, 128, 128);
            const detail::color_int_t light_cyan = detail::resolveColorInt(224, 255, 255);
            const detail::color_int_t light_goldenrod = detail::resolveColorInt(238, 221, 130);
            const detail::color_int_t light_goldenrod_yellow = detail::resolveColorInt(250, 250, 210);
            const detail::color_int_t light_gray = detail::resolveColorInt(211, 211, 211);
            const detail::color_int_t light_green = detail::resolveColorInt(144, 238, 144);
            const detail::color_int_t light_grey = detail::resolveColorInt(211, 211, 211);
            const detail::color_int_t light_pink = detail::resolveColorInt(255, 182, 193);
            const detail::color_int_t light_salmon = detail::resolveColorInt(255, 160, 122);
            const detail::color_int_t light_sea_green = detail::resolveColorInt(32, 178, 170);
            const detail::color_int_t light_sky_blue = detail::resolveColorInt(135, 206, 250);
            const detail::color_int_t light_slate_blue = detail::resolveColorInt(132, 112, 255);
            const detail::color_int_t light_slate_gray = detail::resolveColorInt(119, 136, 153);
            const detail::color_int_t light_slate_grey = detail::resolveColorInt(119, 136, 153);
            const detail::color_int_t light_steel_blue = detail::resolveColorInt(176, 196, 222);
            const detail::color_int_t light_yellow = detail::resolveColorInt(255, 255, 224);
            const detail::color_int_t LightBlue = detail::resolveColorInt(173, 216, 230);
            const detail::color_int_t LightBlue1 = detail::resolveColorInt(191, 239, 255);
            const detail::color_int_t LightBlue2 = detail::resolveColorInt(178, 223, 238);
            const detail::color_int_t LightBlue3 = detail::resolveColorInt(154, 192, 205);
            const detail::color_int_t LightBlue4 = detail::resolveColorInt(104, 131, 139);
            const detail::color_int_t LightCoral = detail::resolveColorInt(240, 128, 128);
            const detail::color_int_t LightCyan = detail::resolveColorInt(224, 255, 255);
            const detail::color_int_t LightCyan1 = detail::resolveColorInt(224, 255, 255);
            const detail::color_int_t LightCyan2 = detail::resolveColorInt(209, 238, 238);
            const detail::color_int_t LightCyan3 = detail::resolveColorInt(180, 205, 205);
            const detail::color_int_t LightCyan4 = detail::resolveColorInt(122, 139, 139);
            const detail::color_int_t LightGoldenrod = detail::resolveColorInt(238, 221, 130);
            const detail::color_int_t LightGoldenrod1 = detail::resolveColorInt(255, 236, 139);
            const detail::color_int_t LightGoldenrod2 = detail::resolveColorInt(238, 220, 130);
            const detail::color_int_t LightGoldenrod3 = detail::resolveColorInt(205, 190, 112);
            const detail::color_int_t LightGoldenrod4 = detail::resolveColorInt(139, 129, 76);
            const detail::color_int_t LightGoldenrodYellow = detail::resolveColorInt(250, 250, 210);
            const detail::color_int_t LightGray = detail::resolveColorInt(211, 211, 211);
            const detail::color_int_t LightGreen = detail::resolveColorInt(144, 238, 144);
            const detail::color_int_t LightGrey = detail::resolveColorInt(211, 211, 211);
            const detail::color_int_t LightPink = detail::resolveColorInt(255, 182, 193);
            const detail::color_int_t LightPink1 = detail::resolveColorInt(255, 174, 185);
            const detail::color_int_t LightPink2 = detail::resolveColorInt(238, 162, 173);
            const detail::color_int_t LightPink3 = detail::resolveColorInt(205, 140, 149);
            const detail::color_int_t LightPink4 = detail::resolveColorInt(139, 95, 101);
            const detail::color_int_t LightSalmon = detail::resolveColorInt(255, 160, 122);
            const detail::color_int_t LightSalmon1 = detail::resolveColorInt(255, 160, 122);
            const detail::color_int_t LightSalmon2 = detail::resolveColorInt(238, 149, 114);
            const detail::color_int_t LightSalmon3 = detail::resolveColorInt(205, 129, 98);
            const detail::color_int_t LightSalmon4 = detail::resolveColorInt(139, 87, 66);
            const detail::color_int_t LightSeaGreen = detail::resolveColorInt(32, 178, 170);
            const detail::color_int_t LightSkyBlue = detail::resolveColorInt(135, 206, 250);
            const detail::color_int_t LightSkyBlue1 = detail::resolveColorInt(176, 226, 255);
            const detail::color_int_t LightSkyBlue2 = detail::resolveColorInt(164, 211, 238);
            const detail::color_int_t LightSkyBlue3 = detail::resolveColorInt(141, 182, 205);
            const detail::color_int_t LightSkyBlue4 = detail::resolveColorInt(96, 123, 139);
            const detail::color_int_t LightSlateBlue = detail::resolveColorInt(132, 112, 255);
            const detail::color_int_t LightSlateGray = detail::resolveColorInt(119, 136, 153);
            const detail::color_int_t LightSlateGrey = detail::resolveColorInt(119, 136, 153);
            const detail::color_int_t LightSteelBlue = detail::resolveColorInt(176, 196, 222);
            const detail::color_int_t LightSteelBlue1 = detail::resolveColorInt(202, 225, 255);
            const detail::color_int_t LightSteelBlue2 = detail::resolveColorInt(188, 210, 238);
            const detail::color_int_t LightSteelBlue3 = detail::resolveColorInt(162, 181, 205);
            const detail::color_int_t LightSteelBlue4 = detail::resolveColorInt(110, 123, 139);
            const detail::color_int_t LightYellow = detail::resolveColorInt(255, 255, 224);
            const detail::color_int_t LightYellow1 = detail::resolveColorInt(255, 255, 224);
            const detail::color_int_t LightYellow2 = detail::resolveColorInt(238, 238, 209);
            const detail::color_int_t LightYellow3 = detail::resolveColorInt(205, 205, 180);
            const detail::color_int_t LightYellow4 = detail::resolveColorInt(139, 139, 122);
            const detail::color_int_t lime_green = detail::resolveColorInt(50, 205, 50);
            const detail::color_int_t LimeGreen = detail::resolveColorInt(50, 205, 50);
            const detail::color_int_t linen = detail::resolveColorInt(250, 240, 230);
            const detail::color_int_t magenta = detail::resolveColorInt(255, 0, 255);
            const detail::color_int_t magenta1 = detail::resolveColorInt(255, 0, 255);
            const detail::color_int_t magenta2 = detail::resolveColorInt(238, 0, 238);
            const detail::color_int_t magenta3 = detail::resolveColorInt(205, 0, 205);
            const detail::color_int_t magenta4 = detail::resolveColorInt(139, 0, 139);
            const detail::color_int_t maroon = detail::resolveColorInt(176, 48, 96);
            const detail::color_int_t maroon1 = detail::resolveColorInt(255, 52, 179);
            const detail::color_int_t maroon2 = detail::resolveColorInt(238, 48, 167);
            const detail::color_int_t maroon3 = detail::resolveColorInt(205, 41, 144);
            const detail::color_int_t maroon4 = detail::resolveColorInt(139, 28, 98);
            const detail::color_int_t medium_aquamarine = detail::resolveColorInt(102, 205, 170);
            const detail::color_int_t medium_blue = detail::resolveColorInt(0, 0, 205);
            const detail::color_int_t medium_orchid = detail::resolveColorInt(186, 85, 211);
            const detail::color_int_t medium_purple = detail::resolveColorInt(147, 112, 219);
            const detail::color_int_t medium_sea_green = detail::resolveColorInt(60, 179, 113);
            const detail::color_int_t medium_slate_blue = detail::resolveColorInt(123, 104, 238);
            const detail::color_int_t medium_spring_green = detail::resolveColorInt(0, 250, 154);
            const detail::color_int_t medium_turquoise = detail::resolveColorInt(72, 209, 204);
            const detail::color_int_t medium_violet_red = detail::resolveColorInt(199, 21, 133);
            const detail::color_int_t MediumAquamarine = detail::resolveColorInt(102, 205, 170);
            const detail::color_int_t MediumBlue = detail::resolveColorInt(0, 0, 205);
            const detail::color_int_t MediumOrchid = detail::resolveColorInt(186, 85, 211);
            const detail::color_int_t MediumOrchid1 = detail::resolveColorInt(224, 102, 255);
            const detail::color_int_t MediumOrchid2 = detail::resolveColorInt(209, 95, 238);
            const detail::color_int_t MediumOrchid3 = detail::resolveColorInt(180, 82, 205);
            const detail::color_int_t MediumOrchid4 = detail::resolveColorInt(122, 55, 139);
            const detail::color_int_t MediumPurple = detail::resolveColorInt(147, 112, 219);
            const detail::color_int_t MediumPurple1 = detail::resolveColorInt(171, 130, 255);
            const detail::color_int_t MediumPurple2 = detail::resolveColorInt(159, 121, 238);
            const detail::color_int_t MediumPurple3 = detail::resolveColorInt(137, 104, 205);
            const detail::color_int_t MediumPurple4 = detail::resolveColorInt(93, 71, 139);
            const detail::color_int_t MediumSeaGreen = detail::resolveColorInt(60, 179, 113);
            const detail::color_int_t MediumSlateBlue = detail::resolveColorInt(123, 104, 238);
            const detail::color_int_t MediumSpringGreen = detail::resolveColorInt(0, 250, 154);
            const detail::color_int_t MediumTurquoise = detail::resolveColorInt(72, 209, 204);
            const detail::color_int_t MediumVioletRed = detail::resolveColorInt(199, 21, 133);
            const detail::color_int_t midnight_blue = detail::resolveColorInt(25, 25, 112);
            const detail::color_int_t MidnightBlue = detail::resolveColorInt(25, 25, 112);
            const detail::color_int_t mint_cream = detail::resolveColorInt(245, 255, 250);
            const detail::color_int_t MintCream = detail::resolveColorInt(245, 255, 250);
            const detail::color_int_t misty_rose = detail::resolveColorInt(255, 228, 225);
            const detail::color_int_t MistyRose = detail::resolveColorInt(255, 228, 225);
            const detail::color_int_t MistyRose1 = detail::resolveColorInt(255, 228, 225);
            const detail::color_int_t MistyRose2 = detail::resolveColorInt(238, 213, 210);
            const detail::color_int_t MistyRose3 = detail::resolveColorInt(205, 183, 181);
            const detail::color_int_t MistyRose4 = detail::resolveColorInt(139, 125, 123);
            const detail::color_int_t moccasin = detail::resolveColorInt(255, 228, 181);
            const detail::color_int_t navajo_white = detail::resolveColorInt(255, 222, 173);
            const detail::color_int_t NavajoWhite = detail::resolveColorInt(255, 222, 173);
            const detail::color_int_t NavajoWhite1 = detail::resolveColorInt(255, 222, 173);
            const detail::color_int_t NavajoWhite2 = detail::resolveColorInt(238, 207, 161);
            const detail::color_int_t NavajoWhite3 = detail::resolveColorInt(205, 179, 139);
            const detail::color_int_t NavajoWhite4 = detail::resolveColorInt(139, 121, 94);
            const detail::color_int_t navy = detail::resolveColorInt(0, 0, 128);
            const detail::color_int_t navy_blue = detail::resolveColorInt(0, 0, 128);
            const detail::color_int_t NavyBlue = detail::resolveColorInt(0, 0, 128);
            const detail::color_int_t old_lace = detail::resolveColorInt(253, 245, 230);
            const detail::color_int_t OldLace = detail::resolveColorInt(253, 245, 230);
            const detail::color_int_t olive_drab = detail::resolveColorInt(107, 142, 35);
            const detail::color_int_t OliveDrab = detail::resolveColorInt(107, 142, 35);
            const detail::color_int_t OliveDrab1 = detail::resolveColorInt(192, 255, 62);
            const detail::color_int_t OliveDrab2 = detail::resolveColorInt(179, 238, 58);
            const detail::color_int_t OliveDrab3 = detail::resolveColorInt(154, 205, 50);
            const detail::color_int_t OliveDrab4 = detail::resolveColorInt(105, 139, 34);
            const detail::color_int_t orange = detail::resolveColorInt(255, 165, 0);
            const detail::color_int_t orange_red = detail::resolveColorInt(255, 69, 0);
            const detail::color_int_t orange1 = detail::resolveColorInt(255, 165, 0);
            const detail::color_int_t orange2 = detail::resolveColorInt(238, 154, 0);
            const detail::color_int_t orange3 = detail::resolveColorInt(205, 133, 0);
            const detail::color_int_t orange4 = detail::resolveColorInt(139, 90, 0);
            const detail::color_int_t OrangeRed = detail::resolveColorInt(255, 69, 0);
            const detail::color_int_t OrangeRed1 = detail::resolveColorInt(255, 69, 0);
            const detail::color_int_t OrangeRed2 = detail::resolveColorInt(238, 64, 0);
            const detail::color_int_t OrangeRed3 = detail::resolveColorInt(205, 55, 0);
            const detail::color_int_t OrangeRed4 = detail::resolveColorInt(139, 37, 0);
            const detail::color_int_t orchid = detail::resolveColorInt(218, 112, 214);
            const detail::color_int_t orchid1 = detail::resolveColorInt(255, 131, 250);
            const detail::color_int_t orchid2 = detail::resolveColorInt(238, 122, 233);
            const detail::color_int_t orchid3 = detail::resolveColorInt(205, 105, 201);
            const detail::color_int_t orchid4 = detail::resolveColorInt(139, 71, 137);
            const detail::color_int_t pale_goldenrod = detail::resolveColorInt(238, 232, 170);
            const detail::color_int_t pale_green = detail::resolveColorInt(152, 251, 152);
            const detail::color_int_t pale_turquoise = detail::resolveColorInt(175, 238, 238);
            const detail::color_int_t pale_violet_red = detail::resolveColorInt(219, 112, 147);
            const detail::color_int_t PaleGoldenrod = detail::resolveColorInt(238, 232, 170);
            const detail::color_int_t PaleGreen = detail::resolveColorInt(152, 251, 152);
            const detail::color_int_t PaleGreen1 = detail::resolveColorInt(154, 255, 154);
            const detail::color_int_t PaleGreen2 = detail::resolveColorInt(144, 238, 144);
            const detail::color_int_t PaleGreen3 = detail::resolveColorInt(124, 205, 124);
            const detail::color_int_t PaleGreen4 = detail::resolveColorInt(84, 139, 84);
            const detail::color_int_t PaleTurquoise = detail::resolveColorInt(175, 238, 238);
            const detail::color_int_t PaleTurquoise1 = detail::resolveColorInt(187, 255, 255);
            const detail::color_int_t PaleTurquoise2 = detail::resolveColorInt(174, 238, 238);
            const detail::color_int_t PaleTurquoise3 = detail::resolveColorInt(150, 205, 205);
            const detail::color_int_t PaleTurquoise4 = detail::resolveColorInt(102, 139, 139);
            const detail::color_int_t PaleVioletRed = detail::resolveColorInt(219, 112, 147);
            const detail::color_int_t PaleVioletRed1 = detail::resolveColorInt(255, 130, 171);
            const detail::color_int_t PaleVioletRed2 = detail::resolveColorInt(238, 121, 159);
            const detail::color_int_t PaleVioletRed3 = detail::resolveColorInt(205, 104, 127);
            const detail::color_int_t PaleVioletRed4 = detail::resolveColorInt(139, 71, 93);
            const detail::color_int_t papaya_whip = detail::resolveColorInt(255, 239, 213);
            const detail::color_int_t PapayaWhip = detail::resolveColorInt(255, 239, 213);
            const detail::color_int_t peach_puff = detail::resolveColorInt(255, 218, 185);
            const detail::color_int_t PeachPuff = detail::resolveColorInt(255, 218, 185);
            const detail::color_int_t PeachPuff1 = detail::resolveColorInt(255, 218, 185);
            const detail::color_int_t PeachPuff2 = detail::resolveColorInt(238, 203, 173);
            const detail::color_int_t PeachPuff3 = detail::resolveColorInt(205, 175, 149);
            const detail::color_int_t PeachPuff4 = detail::resolveColorInt(139, 119, 101);
            const detail::color_int_t peru = detail::resolveColorInt(205, 133, 63);
            const detail::color_int_t pink = detail::resolveColorInt(255, 192, 203);
            const detail::color_int_t pink1 = detail::resolveColorInt(255, 181, 197);
            const detail::color_int_t pink2 = detail::resolveColorInt(238, 169, 184);
            const detail::color_int_t pink3 = detail::resolveColorInt(205, 145, 158);
            const detail::color_int_t pink4 = detail::resolveColorInt(139, 99, 108);
            const detail::color_int_t plum = detail::resolveColorInt(221, 160, 221);
            const detail::color_int_t plum1 = detail::resolveColorInt(255, 187, 255);
            const detail::color_int_t plum2 = detail::resolveColorInt(238, 174, 238);
            const detail::color_int_t plum3 = detail::resolveColorInt(205, 150, 205);
            const detail::color_int_t plum4 = detail::resolveColorInt(139, 102, 139);
            const detail::color_int_t powder_blue = detail::resolveColorInt(176, 224, 230);
            const detail::color_int_t PowderBlue = detail::resolveColorInt(176, 224, 230);
            const detail::color_int_t purple = detail::resolveColorInt(160, 32, 240);
            const detail::color_int_t purple1 = detail::resolveColorInt(155, 48, 255);
            const detail::color_int_t purple2 = detail::resolveColorInt(145, 44, 238);
            const detail::color_int_t purple3 = detail::resolveColorInt(125, 38, 205);
            const detail::color_int_t purple4 = detail::resolveColorInt(85, 26, 139);
            const detail::color_int_t red = detail::resolveColorInt(255, 0, 0);
            const detail::color_int_t red1 = detail::resolveColorInt(255, 0, 0);
            const detail::color_int_t red2 = detail::resolveColorInt(238, 0, 0);
            const detail::color_int_t red3 = detail::resolveColorInt(205, 0, 0);
            const detail::color_int_t red4 = detail::resolveColorInt(139, 0, 0);
            const detail::color_int_t rosy_brown = detail::resolveColorInt(188, 143, 143);
            const detail::color_int_t RosyBrown = detail::resolveColorInt(188, 143, 143);
            const detail::color_int_t RosyBrown1 = detail::resolveColorInt(255, 193, 193);
            const detail::color_int_t RosyBrown2 = detail::resolveColorInt(238, 180, 180);
            const detail::color_int_t RosyBrown3 = detail::resolveColorInt(205, 155, 155);
            const detail::color_int_t RosyBrown4 = detail::resolveColorInt(139, 105, 105);
            const detail::color_int_t royal_blue = detail::resolveColorInt(65, 105, 225);
            const detail::color_int_t RoyalBlue = detail::resolveColorInt(65, 105, 225);
            const detail::color_int_t RoyalBlue1 = detail::resolveColorInt(72, 118, 255);
            const detail::color_int_t RoyalBlue2 = detail::resolveColorInt(67, 110, 238);
            const detail::color_int_t RoyalBlue3 = detail::resolveColorInt(58, 95, 205);
            const detail::color_int_t RoyalBlue4 = detail::resolveColorInt(39, 64, 139);
            const detail::color_int_t saddle_brown = detail::resolveColorInt(139, 69, 19);
            const detail::color_int_t SaddleBrown = detail::resolveColorInt(139, 69, 19);
            const detail::color_int_t salmon = detail::resolveColorInt(250, 128, 114);
            const detail::color_int_t salmon1 = detail::resolveColorInt(255, 140, 105);
            const detail::color_int_t salmon2 = detail::resolveColorInt(238, 130, 98);
            const detail::color_int_t salmon3 = detail::resolveColorInt(205, 112, 84);
            const detail::color_int_t salmon4 = detail::resolveColorInt(139, 76, 57);
            const detail::color_int_t sandy_brown = detail::resolveColorInt(244, 164, 96);
            const detail::color_int_t SandyBrown = detail::resolveColorInt(244, 164, 96);
            const detail::color_int_t sea_green = detail::resolveColorInt(46, 139, 87);
            const detail::color_int_t SeaGreen = detail::resolveColorInt(46, 139, 87);
            const detail::color_int_t SeaGreen1 = detail::resolveColorInt(84, 255, 159);
            const detail::color_int_t SeaGreen2 = detail::resolveColorInt(78, 238, 148);
            const detail::color_int_t SeaGreen3 = detail::resolveColorInt(67, 205, 128);
            const detail::color_int_t SeaGreen4 = detail::resolveColorInt(46, 139, 87);
            const detail::color_int_t seashell = detail::resolveColorInt(255, 245, 238);
            const detail::color_int_t seashell1 = detail::resolveColorInt(255, 245, 238);
            const detail::color_int_t seashell2 = detail::resolveColorInt(238, 229, 222);
            const detail::color_int_t seashell3 = detail::resolveColorInt(205, 197, 191);
            const detail::color_int_t seashell4 = detail::resolveColorInt(139, 134, 130);
            const detail::color_int_t sienna = detail::resolveColorInt(160, 82, 45);
            const detail::color_int_t sienna1 = detail::resolveColorInt(255, 130, 71);
            const detail::color_int_t sienna2 = detail::resolveColorInt(238, 121, 66);
            const detail::color_int_t sienna3 = detail::resolveColorInt(205, 104, 57);
            const detail::color_int_t sienna4 = detail::resolveColorInt(139, 71, 38);
            const detail::color_int_t sky_blue = detail::resolveColorInt(135, 206, 235);
            const detail::color_int_t SkyBlue = detail::resolveColorInt(135, 206, 235);
            const detail::color_int_t SkyBlue1 = detail::resolveColorInt(135, 206, 255);
            const detail::color_int_t SkyBlue2 = detail::resolveColorInt(126, 192, 238);
            const detail::color_int_t SkyBlue3 = detail::resolveColorInt(108, 166, 205);
            const detail::color_int_t SkyBlue4 = detail::resolveColorInt(74, 112, 139);
            const detail::color_int_t slate_blue = detail::resolveColorInt(106, 90, 205);
            const detail::color_int_t slate_gray = detail::resolveColorInt(112, 128, 144);
            const detail::color_int_t slate_grey = detail::resolveColorInt(112, 128, 144);
            const detail::color_int_t SlateBlue = detail::resolveColorInt(106, 90, 205);
            const detail::color_int_t SlateBlue1 = detail::resolveColorInt(131, 111, 255);
            const detail::color_int_t SlateBlue2 = detail::resolveColorInt(122, 103, 238);
            const detail::color_int_t SlateBlue3 = detail::resolveColorInt(105, 89, 205);
            const detail::color_int_t SlateBlue4 = detail::resolveColorInt(71, 60, 139);
            const detail::color_int_t SlateGray = detail::resolveColorInt(112, 128, 144);
            const detail::color_int_t SlateGray1 = detail::resolveColorInt(198, 226, 255);
            const detail::color_int_t SlateGray2 = detail::resolveColorInt(185, 211, 238);
            const detail::color_int_t SlateGray3 = detail::resolveColorInt(159, 182, 205);
            const detail::color_int_t SlateGray4 = detail::resolveColorInt(108, 123, 139);
            const detail::color_int_t SlateGrey = detail::resolveColorInt(112, 128, 144);
            const detail::color_int_t snow = detail::resolveColorInt(255, 250, 250);
            const detail::color_int_t snow1 = detail::resolveColorInt(255, 250, 250);
            const detail::color_int_t snow2 = detail::resolveColorInt(238, 233, 233);
            const detail::color_int_t snow3 = detail::resolveColorInt(205, 201, 201);
            const detail::color_int_t snow4 = detail::resolveColorInt(139, 137, 137);
            const detail::color_int_t spring_green = detail::resolveColorInt(0, 255, 127);
            const detail::color_int_t SpringGreen = detail::resolveColorInt(0, 255, 127);
            const detail::color_int_t SpringGreen1 = detail::resolveColorInt(0, 255, 127);
            const detail::color_int_t SpringGreen2 = detail::resolveColorInt(0, 238, 118);
            const detail::color_int_t SpringGreen3 = detail::resolveColorInt(0, 205, 102);
            const detail::color_int_t SpringGreen4 = detail::resolveColorInt(0, 139, 69);
            const detail::color_int_t steel_blue = detail::resolveColorInt(70, 130, 180);
            const detail::color_int_t SteelBlue = detail::resolveColorInt(70, 130, 180);
            const detail::color_int_t SteelBlue1 = detail::resolveColorInt(99, 184, 255);
            const detail::color_int_t SteelBlue2 = detail::resolveColorInt(92, 172, 238);
            const detail::color_int_t SteelBlue3 = detail::resolveColorInt(79, 148, 205);
            const detail::color_int_t SteelBlue4 = detail::resolveColorInt(54, 100, 139);
            const detail::color_int_t tan = detail::resolveColorInt(210, 180, 140);
            const detail::color_int_t tan1 = detail::resolveColorInt(255, 165, 79);
            const detail::color_int_t tan2 = detail::resolveColorInt(238, 154, 73);
            const detail::color_int_t tan3 = detail::resolveColorInt(205, 133, 63);
            const detail::color_int_t tan4 = detail::resolveColorInt(139, 90, 43);
            const detail::color_int_t thistle = detail::resolveColorInt(216, 191, 216);
            const detail::color_int_t thistle1 = detail::resolveColorInt(255, 225, 255);
            const detail::color_int_t thistle2 = detail::resolveColorInt(238, 210, 238);
            const detail::color_int_t thistle3 = detail::resolveColorInt(205, 181, 205);
            const detail::color_int_t thistle4 = detail::resolveColorInt(139, 123, 139);
            const detail::color_int_t tomato = detail::resolveColorInt(255, 99, 71);
            const detail::color_int_t tomato1 = detail::resolveColorInt(255, 99, 71);
            const detail::color_int_t tomato2 = detail::resolveColorInt(238, 92, 66);
            const detail::color_int_t tomato3 = detail::resolveColorInt(205, 79, 57);
            const detail::color_int_t tomato4 = detail::resolveColorInt(139, 54, 38);
            const detail::color_int_t turquoise = detail::resolveColorInt(64, 224, 208);
            const detail::color_int_t turquoise1 = detail::resolveColorInt(0, 245, 255);
            const detail::color_int_t turquoise2 = detail::resolveColorInt(0, 229, 238);
            const detail::color_int_t turquoise3 = detail::resolveColorInt(0, 197, 205);
            const detail::color_int_t turquoise4 = detail::resolveColorInt(0, 134, 139);
            const detail::color_int_t violet = detail::resolveColorInt(238, 130, 238);
            const detail::color_int_t violet_red = detail::resolveColorInt(208, 32, 144);
            const detail::color_int_t VioletRed = detail::resolveColorInt(208, 32, 144);
            const detail::color_int_t VioletRed1 = detail::resolveColorInt(255, 62, 150);
            const detail::color_int_t VioletRed2 = detail::resolveColorInt(238, 58, 140);
            const detail::color_int_t VioletRed3 = detail::resolveColorInt(205, 50, 120);
            const detail::color_int_t VioletRed4 = detail::resolveColorInt(139, 34, 82);
            const detail::color_int_t wheat = detail::resolveColorInt(245, 222, 179);
            const detail::color_int_t wheat1 = detail::resolveColorInt(255, 231, 186);
            const detail::color_int_t wheat2 = detail::resolveColorInt(238, 216, 174);
            const detail::color_int_t wheat3 = detail::resolveColorInt(205, 186, 150);
            const detail::color_int_t wheat4 = detail::resolveColorInt(139, 126, 102);
            const detail::color_int_t white = detail::resolveColorInt(255, 255, 255);
            const detail::color_int_t white_smoke = detail::resolveColorInt(245, 245, 245);
            const detail::color_int_t WhiteSmoke = detail::resolveColorInt(245, 245, 245);
            const detail::color_int_t yellow = detail::resolveColorInt(255, 255, 0);
            const detail::color_int_t yellow_green = detail::resolveColorInt(154, 205, 50);
            const detail::color_int_t yellow1 = detail::resolveColorInt(255, 255, 0);
            const detail::color_int_t yellow2 = detail::resolveColorInt(238, 238, 0);
            const detail::color_int_t yellow3 = detail::resolveColorInt(205, 205, 0);
            const detail::color_int_t yellow4 = detail::resolveColorInt(139, 139, 0);
            const detail::color_int_t YellowGreen = detail::resolveColorInt(154, 205, 50);
        }
    }

    class Color {
    public:
        typedef uint8_t component_t;

        union {

            struct {
                component_t r;
                component_t g;
                component_t b;
            };
            component_t components[3];
        };

        Color(detail::color_int_t packedColor) {
            detail::resolveColorComp(packedColor, r, g, b);
        }

        /*\brief Color constructor for unsigned 8-bit RGB values.
          \param r Red component.
          \param g Green component.
          \param b Blue component.*/
        Color(component_t r, component_t g, component_t b) :
        r(r), g(g), b(b) {
        };

        /*\brief Copy constructor.
          \param other Constant reference to other instance of a color object.*/
        Color(const Color& other) :
        r(other.r), g(other.g), b(other.b) {
        }

        /*\brief Name constructor.
                         Takes a literal color name as an input.
          \param name The name of the color from which to derive value.
          \sa fromName()*/
        Color(const std::string& name);

        /*\brief Default constructor.
                         Initializes this color to white. (all components 255)*/
        Color() {
            r = g = b = 255;
        }

        Color& operator=(detail::color_int_t pack) {
            detail::resolveColorComp(pack, r, g, b);
            return *this;
        }

        /**\brief Returns a pointer to the first component of this color.
                         This is useful for functions which require color as an input array.
          Returns a read-only pointer to the elements, in sequential order.*/
        const component_t * const rgbPtr() const {
            return &components[0];
        }

        /**\brief Assigns R, G, and B values to the specified pointer.
         * Must contain enough valid space at dest to hold 3 bytes.*/
        void assignAt(component_t* dest) const {
            dest[0] = r;
            dest[1] = g;
            dest[2] = b;
        }
    };

    const std::unordered_map<std::string, detail::color_int_t> NAMED_COLORS = {
        {"alice blue", detail::col::alice_blue},
        {"AliceBlue", detail::col::AliceBlue},
        {"antique white", detail::col::antique_white},
        {"AntiqueWhite", detail::col::AntiqueWhite},
        {"AntiqueWhite1", detail::col::AntiqueWhite1},
        {"AntiqueWhite2", detail::col::AntiqueWhite2},
        {"AntiqueWhite3", detail::col::AntiqueWhite3},
        {"AntiqueWhite4", detail::col::AntiqueWhite4},
        {"aquamarine", detail::col::aquamarine},
        {"aquamarine1", detail::col::aquamarine1},
        {"aquamarine2", detail::col::aquamarine2},
        {"aquamarine3", detail::col::aquamarine3},
        {"aquamarine4", detail::col::aquamarine4},
        {"azure", detail::col::azure},
        {"azure1", detail::col::azure1},
        {"azure2", detail::col::azure2},
        {"azure3", detail::col::azure3},
        {"azure4", detail::col::azure4},
        {"beige", detail::col::beige},
        {"bisque", detail::col::bisque},
        {"bisque1", detail::col::bisque1},
        {"bisque2", detail::col::bisque2},
        {"bisque3", detail::col::bisque3},
        {"bisque4", detail::col::bisque4},
        {"black", detail::col::black},
        {"blanched almond", detail::col::blanched_almond},
        {"BlanchedAlmond", detail::col::BlanchedAlmond},
        {"blue", detail::col::blue},
        {"blue violet", detail::col::blue_violet},
        {"blue1", detail::col::blue1},
        {"blue2", detail::col::blue2},
        {"blue3", detail::col::blue3},
        {"blue4", detail::col::blue4},
        {"BlueViolet", detail::col::BlueViolet},
        {"brown", detail::col::brown},
        {"brown1", detail::col::brown1},
        {"brown2", detail::col::brown2},
        {"brown3", detail::col::brown3},
        {"brown4", detail::col::brown4},
        {"burlywood", detail::col::burlywood},
        {"burlywood1", detail::col::burlywood1},
        {"burlywood2", detail::col::burlywood2},
        {"burlywood3", detail::col::burlywood3},
        {"burlywood4", detail::col::burlywood4},
        {"cadet blue", detail::col::cadet_blue},
        {"CadetBlue", detail::col::CadetBlue},
        {"CadetBlue1", detail::col::CadetBlue1},
        {"CadetBlue2", detail::col::CadetBlue2},
        {"CadetBlue3", detail::col::CadetBlue3},
        {"CadetBlue4", detail::col::CadetBlue4},
        {"chartreuse", detail::col::chartreuse},
        {"chartreuse1", detail::col::chartreuse1},
        {"chartreuse2", detail::col::chartreuse2},
        {"chartreuse3", detail::col::chartreuse3},
        {"chartreuse4", detail::col::chartreuse4},
        {"chocolate", detail::col::chocolate},
        {"chocolate1", detail::col::chocolate1},
        {"chocolate2", detail::col::chocolate2},
        {"chocolate3", detail::col::chocolate3},
        {"chocolate4", detail::col::chocolate4},
        {"coral", detail::col::coral},
        {"coral1", detail::col::coral1},
        {"coral2", detail::col::coral2},
        {"coral3", detail::col::coral3},
        {"coral4", detail::col::coral4},
        {"cornflower blue", detail::col::cornflower_blue},
        {"CornflowerBlue", detail::col::CornflowerBlue},
        {"cornsilk", detail::col::cornsilk},
        {"cornsilk1", detail::col::cornsilk1},
        {"cornsilk2", detail::col::cornsilk2},
        {"cornsilk3", detail::col::cornsilk3},
        {"cornsilk4", detail::col::cornsilk4},
        {"cyan", detail::col::cyan},
        {"cyan1", detail::col::cyan1},
        {"cyan2", detail::col::cyan2},
        {"cyan3", detail::col::cyan3},
        {"cyan4", detail::col::cyan4},
        {"dark blue", detail::col::dark_blue},
        {"dark cyan", detail::col::dark_cyan},
        {"dark goldenrod", detail::col::dark_goldenrod},
        {"dark gray", detail::col::dark_gray},
        {"dark green", detail::col::dark_green},
        {"dark grey", detail::col::dark_grey},
        {"dark khaki", detail::col::dark_khaki},
        {"dark magenta", detail::col::dark_magenta},
        {"dark olive green", detail::col::dark_olive_green},
        {"dark orange", detail::col::dark_orange},
        {"dark orchid", detail::col::dark_orchid},
        {"dark red", detail::col::dark_red},
        {"dark salmon", detail::col::dark_salmon},
        {"dark sea green", detail::col::dark_sea_green},
        {"dark slate blue", detail::col::dark_slate_blue},
        {"dark slate gray", detail::col::dark_slate_gray},
        {"dark slate grey", detail::col::dark_slate_grey},
        {"dark turquoise", detail::col::dark_turquoise},
        {"dark violet", detail::col::dark_violet},
        {"DarkBlue", detail::col::DarkBlue},
        {"DarkCyan", detail::col::DarkCyan},
        {"DarkGoldenrod", detail::col::DarkGoldenrod},
        {"DarkGoldenrod1", detail::col::DarkGoldenrod1},
        {"DarkGoldenrod2", detail::col::DarkGoldenrod2},
        {"DarkGoldenrod3", detail::col::DarkGoldenrod3},
        {"DarkGoldenrod4", detail::col::DarkGoldenrod4},
        {"DarkGray", detail::col::DarkGray},
        {"DarkGreen", detail::col::DarkGreen},
        {"DarkGrey", detail::col::DarkGrey},
        {"DarkKhaki", detail::col::DarkKhaki},
        {"DarkMagenta", detail::col::DarkMagenta},
        {"DarkOliveGreen", detail::col::DarkOliveGreen},
        {"DarkOliveGreen1", detail::col::DarkOliveGreen1},
        {"DarkOliveGreen2", detail::col::DarkOliveGreen2},
        {"DarkOliveGreen3", detail::col::DarkOliveGreen3},
        {"DarkOliveGreen4", detail::col::DarkOliveGreen4},
        {"DarkOrange", detail::col::DarkOrange},
        {"DarkOrange1", detail::col::DarkOrange1},
        {"DarkOrange2", detail::col::DarkOrange2},
        {"DarkOrange3", detail::col::DarkOrange3},
        {"DarkOrange4", detail::col::DarkOrange4},
        {"DarkOrchid", detail::col::DarkOrchid},
        {"DarkOrchid1", detail::col::DarkOrchid1},
        {"DarkOrchid2", detail::col::DarkOrchid2},
        {"DarkOrchid3", detail::col::DarkOrchid3},
        {"DarkOrchid4", detail::col::DarkOrchid4},
        {"DarkRed", detail::col::DarkRed},
        {"DarkSalmon", detail::col::DarkSalmon},
        {"DarkSeaGreen", detail::col::DarkSeaGreen},
        {"DarkSeaGreen1", detail::col::DarkSeaGreen1},
        {"DarkSeaGreen2", detail::col::DarkSeaGreen2},
        {"DarkSeaGreen3", detail::col::DarkSeaGreen3},
        {"DarkSeaGreen4", detail::col::DarkSeaGreen4},
        {"DarkSlateBlue", detail::col::DarkSlateBlue},
        {"DarkSlateGray", detail::col::DarkSlateGray},
        {"DarkSlateGray1", detail::col::DarkSlateGray1},
        {"DarkSlateGray2", detail::col::DarkSlateGray2},
        {"DarkSlateGray3", detail::col::DarkSlateGray3},
        {"DarkSlateGray4", detail::col::DarkSlateGray4},
        {"DarkSlateGrey", detail::col::DarkSlateGrey},
        {"DarkTurquoise", detail::col::DarkTurquoise},
        {"DarkViolet", detail::col::DarkViolet},
        {"deep pink", detail::col::deep_pink},
        {"deep sky blue", detail::col::deep_sky_blue},
        {"DeepPink", detail::col::DeepPink},
        {"DeepPink1", detail::col::DeepPink1},
        {"DeepPink2", detail::col::DeepPink2},
        {"DeepPink3", detail::col::DeepPink3},
        {"DeepPink4", detail::col::DeepPink4},
        {"DeepSkyBlue", detail::col::DeepSkyBlue},
        {"DeepSkyBlue1", detail::col::DeepSkyBlue1},
        {"DeepSkyBlue2", detail::col::DeepSkyBlue2},
        {"DeepSkyBlue3", detail::col::DeepSkyBlue3},
        {"DeepSkyBlue4", detail::col::DeepSkyBlue4},
        {"dim gray", detail::col::dim_gray},
        {"dim grey", detail::col::dim_grey},
        {"DimGray", detail::col::DimGray},
        {"DimGrey", detail::col::DimGrey},
        {"dodger blue", detail::col::dodger_blue},
        {"DodgerBlue", detail::col::DodgerBlue},
        {"DodgerBlue1", detail::col::DodgerBlue1},
        {"DodgerBlue2", detail::col::DodgerBlue2},
        {"DodgerBlue3", detail::col::DodgerBlue3},
        {"DodgerBlue4", detail::col::DodgerBlue4},
        {"firebrick", detail::col::firebrick},
        {"firebrick1", detail::col::firebrick1},
        {"firebrick2", detail::col::firebrick2},
        {"firebrick3", detail::col::firebrick3},
        {"firebrick4", detail::col::firebrick4},
        {"floral white", detail::col::floral_white},
        {"FloralWhite", detail::col::FloralWhite},
        {"forest green", detail::col::forest_green},
        {"ForestGreen", detail::col::ForestGreen},
        {"gainsboro", detail::col::gainsboro},
        {"ghost white", detail::col::ghost_white},
        {"GhostWhite", detail::col::GhostWhite},
        {"gold", detail::col::gold},
        {"gold1", detail::col::gold1},
        {"gold2", detail::col::gold2},
        {"gold3", detail::col::gold3},
        {"gold4", detail::col::gold4},
        {"goldenrod", detail::col::goldenrod},
        {"goldenrod1", detail::col::goldenrod1},
        {"goldenrod2", detail::col::goldenrod2},
        {"goldenrod3", detail::col::goldenrod3},
        {"goldenrod4", detail::col::goldenrod4},
        {"gray", detail::col::gray},
        {"gray0", detail::col::gray0},
        {"gray1", detail::col::gray1},
        {"gray2", detail::col::gray2},
        {"gray3", detail::col::gray3},
        {"gray4", detail::col::gray4},
        {"gray5", detail::col::gray5},
        {"gray6", detail::col::gray6},
        {"gray7", detail::col::gray7},
        {"gray8", detail::col::gray8},
        {"gray9", detail::col::gray9},
        {"gray10", detail::col::gray10},
        {"gray11", detail::col::gray11},
        {"gray12", detail::col::gray12},
        {"gray13", detail::col::gray13},
        {"gray14", detail::col::gray14},
        {"gray15", detail::col::gray15},
        {"gray16", detail::col::gray16},
        {"gray17", detail::col::gray17},
        {"gray18", detail::col::gray18},
        {"gray19", detail::col::gray19},
        {"gray20", detail::col::gray20},
        {"gray21", detail::col::gray21},
        {"gray22", detail::col::gray22},
        {"gray23", detail::col::gray23},
        {"gray24", detail::col::gray24},
        {"gray25", detail::col::gray25},
        {"gray26", detail::col::gray26},
        {"gray27", detail::col::gray27},
        {"gray28", detail::col::gray28},
        {"gray29", detail::col::gray29},
        {"gray30", detail::col::gray30},
        {"gray31", detail::col::gray31},
        {"gray32", detail::col::gray32},
        {"gray33", detail::col::gray33},
        {"gray34", detail::col::gray34},
        {"gray35", detail::col::gray35},
        {"gray36", detail::col::gray36},
        {"gray37", detail::col::gray37},
        {"gray38", detail::col::gray38},
        {"gray39", detail::col::gray39},
        {"gray40", detail::col::gray40},
        {"gray41", detail::col::gray41},
        {"gray42", detail::col::gray42},
        {"gray43", detail::col::gray43},
        {"gray44", detail::col::gray44},
        {"gray45", detail::col::gray45},
        {"gray46", detail::col::gray46},
        {"gray47", detail::col::gray47},
        {"gray48", detail::col::gray48},
        {"gray49", detail::col::gray49},
        {"gray50", detail::col::gray50},
        {"gray51", detail::col::gray51},
        {"gray52", detail::col::gray52},
        {"gray53", detail::col::gray53},
        {"gray54", detail::col::gray54},
        {"gray55", detail::col::gray55},
        {"gray56", detail::col::gray56},
        {"gray57", detail::col::gray57},
        {"gray58", detail::col::gray58},
        {"gray59", detail::col::gray59},
        {"gray60", detail::col::gray60},
        {"gray61", detail::col::gray61},
        {"gray62", detail::col::gray62},
        {"gray63", detail::col::gray63},
        {"gray64", detail::col::gray64},
        {"gray65", detail::col::gray65},
        {"gray66", detail::col::gray66},
        {"gray67", detail::col::gray67},
        {"gray68", detail::col::gray68},
        {"gray69", detail::col::gray69},
        {"gray70", detail::col::gray70},
        {"gray71", detail::col::gray71},
        {"gray72", detail::col::gray72},
        {"gray73", detail::col::gray73},
        {"gray74", detail::col::gray74},
        {"gray75", detail::col::gray75},
        {"gray76", detail::col::gray76},
        {"gray77", detail::col::gray77},
        {"gray78", detail::col::gray78},
        {"gray79", detail::col::gray79},
        {"gray80", detail::col::gray80},
        {"gray81", detail::col::gray81},
        {"gray82", detail::col::gray82},
        {"gray83", detail::col::gray83},
        {"gray84", detail::col::gray84},
        {"gray85", detail::col::gray85},
        {"gray86", detail::col::gray86},
        {"gray87", detail::col::gray87},
        {"gray88", detail::col::gray88},
        {"gray89", detail::col::gray89},
        {"gray90", detail::col::gray90},
        {"gray91", detail::col::gray91},
        {"gray92", detail::col::gray92},
        {"gray93", detail::col::gray93},
        {"gray94", detail::col::gray94},
        {"gray95", detail::col::gray95},
        {"gray96", detail::col::gray96},
        {"gray97", detail::col::gray97},
        {"gray98", detail::col::gray98},
        {"gray99", detail::col::gray99},
        {"gray100", detail::col::gray100},
        {"green", detail::col::green},
        {"green yellow", detail::col::green_yellow},
        {"green1", detail::col::green1},
        {"green2", detail::col::green2},
        {"green3", detail::col::green3},
        {"green4", detail::col::green4},
        {"GreenYellow", detail::col::GreenYellow},
        {"grey", detail::col::grey},
        {"grey0", detail::col::grey0},
        {"grey1", detail::col::grey1},
        {"grey2", detail::col::grey2},
        {"grey3", detail::col::grey3},
        {"grey4", detail::col::grey4},
        {"grey5", detail::col::grey5},
        {"grey6", detail::col::grey6},
        {"grey7", detail::col::grey7},
        {"grey8", detail::col::grey8},
        {"grey9", detail::col::grey9},
        {"grey10", detail::col::grey10},
        {"grey11", detail::col::grey11},
        {"grey12", detail::col::grey12},
        {"grey13", detail::col::grey13},
        {"grey14", detail::col::grey14},
        {"grey15", detail::col::grey15},
        {"grey16", detail::col::grey16},
        {"grey17", detail::col::grey17},
        {"grey18", detail::col::grey18},
        {"grey19", detail::col::grey19},
        {"grey20", detail::col::grey20},
        {"grey21", detail::col::grey21},
        {"grey22", detail::col::grey22},
        {"grey23", detail::col::grey23},
        {"grey24", detail::col::grey24},
        {"grey25", detail::col::grey25},
        {"grey26", detail::col::grey26},
        {"grey27", detail::col::grey27},
        {"grey28", detail::col::grey28},
        {"grey29", detail::col::grey29},
        {"grey30", detail::col::grey30},
        {"grey31", detail::col::grey31},
        {"grey32", detail::col::grey32},
        {"grey33", detail::col::grey33},
        {"grey34", detail::col::grey34},
        {"grey35", detail::col::grey35},
        {"grey36", detail::col::grey36},
        {"grey37", detail::col::grey37},
        {"grey38", detail::col::grey38},
        {"grey39", detail::col::grey39},
        {"grey40", detail::col::grey40},
        {"grey41", detail::col::grey41},
        {"grey42", detail::col::grey42},
        {"grey43", detail::col::grey43},
        {"grey44", detail::col::grey44},
        {"grey45", detail::col::grey45},
        {"grey46", detail::col::grey46},
        {"grey47", detail::col::grey47},
        {"grey48", detail::col::grey48},
        {"grey49", detail::col::grey49},
        {"grey50", detail::col::grey50},
        {"grey51", detail::col::grey51},
        {"grey52", detail::col::grey52},
        {"grey53", detail::col::grey53},
        {"grey54", detail::col::grey54},
        {"grey55", detail::col::grey55},
        {"grey56", detail::col::grey56},
        {"grey57", detail::col::grey57},
        {"grey58", detail::col::grey58},
        {"grey59", detail::col::grey59},
        {"grey60", detail::col::grey60},
        {"grey61", detail::col::grey61},
        {"grey62", detail::col::grey62},
        {"grey63", detail::col::grey63},
        {"grey64", detail::col::grey64},
        {"grey65", detail::col::grey65},
        {"grey66", detail::col::grey66},
        {"grey67", detail::col::grey67},
        {"grey68", detail::col::grey68},
        {"grey69", detail::col::grey69},
        {"grey70", detail::col::grey70},
        {"grey71", detail::col::grey71},
        {"grey72", detail::col::grey72},
        {"grey73", detail::col::grey73},
        {"grey74", detail::col::grey74},
        {"grey75", detail::col::grey75},
        {"grey76", detail::col::grey76},
        {"grey77", detail::col::grey77},
        {"grey78", detail::col::grey78},
        {"grey79", detail::col::grey79},
        {"grey80", detail::col::grey80},
        {"grey81", detail::col::grey81},
        {"grey82", detail::col::grey82},
        {"grey83", detail::col::grey83},
        {"grey84", detail::col::grey84},
        {"grey85", detail::col::grey85},
        {"grey86", detail::col::grey86},
        {"grey87", detail::col::grey87},
        {"grey88", detail::col::grey88},
        {"grey89", detail::col::grey89},
        {"grey90", detail::col::grey90},
        {"grey91", detail::col::grey91},
        {"grey92", detail::col::grey92},
        {"grey93", detail::col::grey93},
        {"grey94", detail::col::grey94},
        {"grey95", detail::col::grey95},
        {"grey96", detail::col::grey96},
        {"grey97", detail::col::grey97},
        {"grey98", detail::col::grey98},
        {"grey99", detail::col::grey99},
        {"grey100", detail::col::grey100},
        {"honeydew", detail::col::honeydew},
        {"honeydew1", detail::col::honeydew1},
        {"honeydew2", detail::col::honeydew2},
        {"honeydew3", detail::col::honeydew3},
        {"honeydew4", detail::col::honeydew4},
        {"hot pink", detail::col::hot_pink},
        {"HotPink", detail::col::HotPink},
        {"HotPink1", detail::col::HotPink1},
        {"HotPink2", detail::col::HotPink2},
        {"HotPink3", detail::col::HotPink3},
        {"HotPink4", detail::col::HotPink4},
        {"indian red", detail::col::indian_red},
        {"IndianRed", detail::col::IndianRed},
        {"IndianRed1", detail::col::IndianRed1},
        {"IndianRed2", detail::col::IndianRed2},
        {"IndianRed3", detail::col::IndianRed3},
        {"IndianRed4", detail::col::IndianRed4},
        {"ivory", detail::col::ivory},
        {"ivory1", detail::col::ivory1},
        {"ivory2", detail::col::ivory2},
        {"ivory3", detail::col::ivory3},
        {"ivory4", detail::col::ivory4},
        {"khaki", detail::col::khaki},
        {"khaki1", detail::col::khaki1},
        {"khaki2", detail::col::khaki2},
        {"khaki3", detail::col::khaki3},
        {"khaki4", detail::col::khaki4},
        {"lavender", detail::col::lavender},
        {"lavender blush", detail::col::lavender_blush},
        {"LavenderBlush", detail::col::LavenderBlush},
        {"LavenderBlush1", detail::col::LavenderBlush1},
        {"LavenderBlush2", detail::col::LavenderBlush2},
        {"LavenderBlush3", detail::col::LavenderBlush3},
        {"LavenderBlush4", detail::col::LavenderBlush4},
        {"lawn green", detail::col::lawn_green},
        {"LawnGreen", detail::col::LawnGreen},
        {"lemon chiffon", detail::col::lemon_chiffon},
        {"LemonChiffon", detail::col::LemonChiffon},
        {"LemonChiffon1", detail::col::LemonChiffon1},
        {"LemonChiffon2", detail::col::LemonChiffon2},
        {"LemonChiffon3", detail::col::LemonChiffon3},
        {"LemonChiffon4", detail::col::LemonChiffon4},
        {"light blue", detail::col::light_blue},
        {"light coral", detail::col::light_coral},
        {"light cyan", detail::col::light_cyan},
        {"light goldenrod", detail::col::light_goldenrod},
        {"light goldenrod yellow", detail::col::light_goldenrod_yellow},
        {"light gray", detail::col::light_gray},
        {"light green", detail::col::light_green},
        {"light grey", detail::col::light_grey},
        {"light pink", detail::col::light_pink},
        {"light salmon", detail::col::light_salmon},
        {"light sea green", detail::col::light_sea_green},
        {"light sky blue", detail::col::light_sky_blue},
        {"light slate blue", detail::col::light_slate_blue},
        {"light slate gray", detail::col::light_slate_gray},
        {"light slate grey", detail::col::light_slate_grey},
        {"light steel blue", detail::col::light_steel_blue},
        {"light yellow", detail::col::light_yellow},
        {"LightBlue", detail::col::LightBlue},
        {"LightBlue1", detail::col::LightBlue1},
        {"LightBlue2", detail::col::LightBlue2},
        {"LightBlue3", detail::col::LightBlue3},
        {"LightBlue4", detail::col::LightBlue4},
        {"LightCoral", detail::col::LightCoral},
        {"LightCyan", detail::col::LightCyan},
        {"LightCyan1", detail::col::LightCyan1},
        {"LightCyan2", detail::col::LightCyan2},
        {"LightCyan3", detail::col::LightCyan3},
        {"LightCyan4", detail::col::LightCyan4},
        {"LightGoldenrod", detail::col::LightGoldenrod},
        {"LightGoldenrod1", detail::col::LightGoldenrod1},
        {"LightGoldenrod2", detail::col::LightGoldenrod2},
        {"LightGoldenrod3", detail::col::LightGoldenrod3},
        {"LightGoldenrod4", detail::col::LightGoldenrod4},
        {"LightGoldenrodYellow", detail::col::LightGoldenrodYellow},
        {"LightGray", detail::col::LightGray},
        {"LightGreen", detail::col::LightGreen},
        {"LightGrey", detail::col::LightGrey},
        {"LightPink", detail::col::LightPink},
        {"LightPink1", detail::col::LightPink1},
        {"LightPink2", detail::col::LightPink2},
        {"LightPink3", detail::col::LightPink3},
        {"LightPink4", detail::col::LightPink4},
        {"LightSalmon", detail::col::LightSalmon},
        {"LightSalmon1", detail::col::LightSalmon1},
        {"LightSalmon2", detail::col::LightSalmon2},
        {"LightSalmon3", detail::col::LightSalmon3},
        {"LightSalmon4", detail::col::LightSalmon4},
        {"LightSeaGreen", detail::col::LightSeaGreen},
        {"LightSkyBlue", detail::col::LightSkyBlue},
        {"LightSkyBlue1", detail::col::LightSkyBlue1},
        {"LightSkyBlue2", detail::col::LightSkyBlue2},
        {"LightSkyBlue3", detail::col::LightSkyBlue3},
        {"LightSkyBlue4", detail::col::LightSkyBlue4},
        {"LightSlateBlue", detail::col::LightSlateBlue},
        {"LightSlateGray", detail::col::LightSlateGray},
        {"LightSlateGrey", detail::col::LightSlateGrey},
        {"LightSteelBlue", detail::col::LightSteelBlue},
        {"LightSteelBlue1", detail::col::LightSteelBlue1},
        {"LightSteelBlue2", detail::col::LightSteelBlue2},
        {"LightSteelBlue3", detail::col::LightSteelBlue3},
        {"LightSteelBlue4", detail::col::LightSteelBlue4},
        {"LightYellow", detail::col::LightYellow},
        {"LightYellow1", detail::col::LightYellow1},
        {"LightYellow2", detail::col::LightYellow2},
        {"LightYellow3", detail::col::LightYellow3},
        {"LightYellow4", detail::col::LightYellow4},
        {"lime green", detail::col::lime_green},
        {"LimeGreen", detail::col::LimeGreen},
        {"linen", detail::col::linen},
        {"magenta", detail::col::magenta},
        {"magenta1", detail::col::magenta1},
        {"magenta2", detail::col::magenta2},
        {"magenta3", detail::col::magenta3},
        {"magenta4", detail::col::magenta4},
        {"maroon", detail::col::maroon},
        {"maroon1", detail::col::maroon1},
        {"maroon2", detail::col::maroon2},
        {"maroon3", detail::col::maroon3},
        {"maroon4", detail::col::maroon4},
        {"medium aquamarine", detail::col::medium_aquamarine},
        {"medium blue", detail::col::medium_blue},
        {"medium orchid", detail::col::medium_orchid},
        {"medium purple", detail::col::medium_purple},
        {"medium sea green", detail::col::medium_sea_green},
        {"medium slate blue", detail::col::medium_slate_blue},
        {"medium spring green", detail::col::medium_spring_green},
        {"medium turquoise", detail::col::medium_turquoise},
        {"medium violet red", detail::col::medium_violet_red},
        {"MediumAquamarine", detail::col::MediumAquamarine},
        {"MediumBlue", detail::col::MediumBlue},
        {"MediumOrchid", detail::col::MediumOrchid},
        {"MediumOrchid1", detail::col::MediumOrchid1},
        {"MediumOrchid2", detail::col::MediumOrchid2},
        {"MediumOrchid3", detail::col::MediumOrchid3},
        {"MediumOrchid4", detail::col::MediumOrchid4},
        {"MediumPurple", detail::col::MediumPurple},
        {"MediumPurple1", detail::col::MediumPurple1},
        {"MediumPurple2", detail::col::MediumPurple2},
        {"MediumPurple3", detail::col::MediumPurple3},
        {"MediumPurple4", detail::col::MediumPurple4},
        {"MediumSeaGreen", detail::col::MediumSeaGreen},
        {"MediumSlateBlue", detail::col::MediumSlateBlue},
        {"MediumSpringGreen", detail::col::MediumSpringGreen},
        {"MediumTurquoise", detail::col::MediumTurquoise},
        {"MediumVioletRed", detail::col::MediumVioletRed},
        {"midnight blue", detail::col::midnight_blue},
        {"MidnightBlue", detail::col::MidnightBlue},
        {"mint cream", detail::col::mint_cream},
        {"MintCream", detail::col::MintCream},
        {"misty rose", detail::col::misty_rose},
        {"MistyRose", detail::col::MistyRose},
        {"MistyRose1", detail::col::MistyRose1},
        {"MistyRose2", detail::col::MistyRose2},
        {"MistyRose3", detail::col::MistyRose3},
        {"MistyRose4", detail::col::MistyRose4},
        {"moccasin", detail::col::moccasin},
        {"navajo white", detail::col::navajo_white},
        {"NavajoWhite", detail::col::NavajoWhite},
        {"NavajoWhite1", detail::col::NavajoWhite1},
        {"NavajoWhite2", detail::col::NavajoWhite2},
        {"NavajoWhite3", detail::col::NavajoWhite3},
        {"NavajoWhite4", detail::col::NavajoWhite4},
        {"navy", detail::col::navy},
        {"navy blue", detail::col::navy_blue},
        {"NavyBlue", detail::col::NavyBlue},
        {"old lace", detail::col::old_lace},
        {"OldLace", detail::col::OldLace},
        {"olive drab", detail::col::olive_drab},
        {"OliveDrab", detail::col::OliveDrab},
        {"OliveDrab1", detail::col::OliveDrab1},
        {"OliveDrab2", detail::col::OliveDrab2},
        {"OliveDrab3", detail::col::OliveDrab3},
        {"OliveDrab4", detail::col::OliveDrab4},
        {"orange", detail::col::orange},
        {"orange red", detail::col::orange_red},
        {"orange1", detail::col::orange1},
        {"orange2", detail::col::orange2},
        {"orange3", detail::col::orange3},
        {"orange4", detail::col::orange4},
        {"OrangeRed", detail::col::OrangeRed},
        {"OrangeRed1", detail::col::OrangeRed1},
        {"OrangeRed2", detail::col::OrangeRed2},
        {"OrangeRed3", detail::col::OrangeRed3},
        {"OrangeRed4", detail::col::OrangeRed4},
        {"orchid", detail::col::orchid},
        {"orchid1", detail::col::orchid1},
        {"orchid2", detail::col::orchid2},
        {"orchid3", detail::col::orchid3},
        {"orchid4", detail::col::orchid4},
        {"pale goldenrod", detail::col::pale_goldenrod},
        {"pale green", detail::col::pale_green},
        {"pale turquoise", detail::col::pale_turquoise},
        {"pale violet red", detail::col::pale_violet_red},
        {"PaleGoldenrod", detail::col::PaleGoldenrod},
        {"PaleGreen", detail::col::PaleGreen},
        {"PaleGreen1", detail::col::PaleGreen1},
        {"PaleGreen2", detail::col::PaleGreen2},
        {"PaleGreen3", detail::col::PaleGreen3},
        {"PaleGreen4", detail::col::PaleGreen4},
        {"PaleTurquoise", detail::col::PaleTurquoise},
        {"PaleTurquoise1", detail::col::PaleTurquoise1},
        {"PaleTurquoise2", detail::col::PaleTurquoise2},
        {"PaleTurquoise3", detail::col::PaleTurquoise3},
        {"PaleTurquoise4", detail::col::PaleTurquoise4},
        {"PaleVioletRed", detail::col::PaleVioletRed},
        {"PaleVioletRed1", detail::col::PaleVioletRed1},
        {"PaleVioletRed2", detail::col::PaleVioletRed2},
        {"PaleVioletRed3", detail::col::PaleVioletRed3},
        {"PaleVioletRed4", detail::col::PaleVioletRed4},
        {"papaya whip", detail::col::papaya_whip},
        {"PapayaWhip", detail::col::PapayaWhip},
        {"peach puff", detail::col::peach_puff},
        {"PeachPuff", detail::col::PeachPuff},
        {"PeachPuff1", detail::col::PeachPuff1},
        {"PeachPuff2", detail::col::PeachPuff2},
        {"PeachPuff3", detail::col::PeachPuff3},
        {"PeachPuff4", detail::col::PeachPuff4},
        {"peru", detail::col::peru},
        {"pink", detail::col::pink},
        {"pink1", detail::col::pink1},
        {"pink2", detail::col::pink2},
        {"pink3", detail::col::pink3},
        {"pink4", detail::col::pink4},
        {"plum", detail::col::plum},
        {"plum1", detail::col::plum1},
        {"plum2", detail::col::plum2},
        {"plum3", detail::col::plum3},
        {"plum4", detail::col::plum4},
        {"powder blue", detail::col::powder_blue},
        {"PowderBlue", detail::col::PowderBlue},
        {"purple", detail::col::purple},
        {"purple1", detail::col::purple1},
        {"purple2", detail::col::purple2},
        {"purple3", detail::col::purple3},
        {"purple4", detail::col::purple4},
        {"red", detail::col::red},
        {"red1", detail::col::red1},
        {"red2", detail::col::red2},
        {"red3", detail::col::red3},
        {"red4", detail::col::red4},
        {"rosy brown", detail::col::rosy_brown},
        {"RosyBrown", detail::col::RosyBrown},
        {"RosyBrown1", detail::col::RosyBrown1},
        {"RosyBrown2", detail::col::RosyBrown2},
        {"RosyBrown3", detail::col::RosyBrown3},
        {"RosyBrown4", detail::col::RosyBrown4},
        {"royal blue", detail::col::royal_blue},
        {"RoyalBlue", detail::col::RoyalBlue},
        {"RoyalBlue1", detail::col::RoyalBlue1},
        {"RoyalBlue2", detail::col::RoyalBlue2},
        {"RoyalBlue3", detail::col::RoyalBlue3},
        {"RoyalBlue4", detail::col::RoyalBlue4},
        {"saddle brown", detail::col::saddle_brown},
        {"SaddleBrown", detail::col::SaddleBrown},
        {"salmon", detail::col::salmon},
        {"salmon1", detail::col::salmon1},
        {"salmon2", detail::col::salmon2},
        {"salmon3", detail::col::salmon3},
        {"salmon4", detail::col::salmon4},
        {"sandy brown", detail::col::sandy_brown},
        {"SandyBrown", detail::col::SandyBrown},
        {"sea green", detail::col::sea_green},
        {"SeaGreen", detail::col::SeaGreen},
        {"SeaGreen1", detail::col::SeaGreen1},
        {"SeaGreen2", detail::col::SeaGreen2},
        {"SeaGreen3", detail::col::SeaGreen3},
        {"SeaGreen4", detail::col::SeaGreen4},
        {"seashell", detail::col::seashell},
        {"seashell1", detail::col::seashell1},
        {"seashell2", detail::col::seashell2},
        {"seashell3", detail::col::seashell3},
        {"seashell4", detail::col::seashell4},
        {"sienna", detail::col::sienna},
        {"sienna1", detail::col::sienna1},
        {"sienna2", detail::col::sienna2},
        {"sienna3", detail::col::sienna3},
        {"sienna4", detail::col::sienna4},
        {"sky blue", detail::col::sky_blue},
        {"SkyBlue", detail::col::SkyBlue},
        {"SkyBlue1", detail::col::SkyBlue1},
        {"SkyBlue2", detail::col::SkyBlue2},
        {"SkyBlue3", detail::col::SkyBlue3},
        {"SkyBlue4", detail::col::SkyBlue4},
        {"slate blue", detail::col::slate_blue},
        {"slate gray", detail::col::slate_gray},
        {"slate grey", detail::col::slate_grey},
        {"SlateBlue", detail::col::SlateBlue},
        {"SlateBlue1", detail::col::SlateBlue1},
        {"SlateBlue2", detail::col::SlateBlue2},
        {"SlateBlue3", detail::col::SlateBlue3},
        {"SlateBlue4", detail::col::SlateBlue4},
        {"SlateGray", detail::col::SlateGray},
        {"SlateGray1", detail::col::SlateGray1},
        {"SlateGray2", detail::col::SlateGray2},
        {"SlateGray3", detail::col::SlateGray3},
        {"SlateGray4", detail::col::SlateGray4},
        {"SlateGrey", detail::col::SlateGrey},
        {"snow", detail::col::snow},
        {"snow1", detail::col::snow1},
        {"snow2", detail::col::snow2},
        {"snow3", detail::col::snow3},
        {"snow4", detail::col::snow4},
        {"spring green", detail::col::spring_green},
        {"SpringGreen", detail::col::SpringGreen},
        {"SpringGreen1", detail::col::SpringGreen1},
        {"SpringGreen2", detail::col::SpringGreen2},
        {"SpringGreen3", detail::col::SpringGreen3},
        {"SpringGreen4", detail::col::SpringGreen4},
        {"steel blue", detail::col::steel_blue},
        {"SteelBlue", detail::col::SteelBlue},
        {"SteelBlue1", detail::col::SteelBlue1},
        {"SteelBlue2", detail::col::SteelBlue2},
        {"SteelBlue3", detail::col::SteelBlue3},
        {"SteelBlue4", detail::col::SteelBlue4},
        {"tan", detail::col::tan},
        {"tan1", detail::col::tan1},
        {"tan2", detail::col::tan2},
        {"tan3", detail::col::tan3},
        {"tan4", detail::col::tan4},
        {"thistle", detail::col::thistle},
        {"thistle1", detail::col::thistle1},
        {"thistle2", detail::col::thistle2},
        {"thistle3", detail::col::thistle3},
        {"thistle4", detail::col::thistle4},
        {"tomato", detail::col::tomato},
        {"tomato1", detail::col::tomato1},
        {"tomato2", detail::col::tomato2},
        {"tomato3", detail::col::tomato3},
        {"tomato4", detail::col::tomato4},
        {"turquoise", detail::col::turquoise},
        {"turquoise1", detail::col::turquoise1},
        {"turquoise2", detail::col::turquoise2},
        {"turquoise3", detail::col::turquoise3},
        {"turquoise4", detail::col::turquoise4},
        {"violet", detail::col::violet},
        {"violet red", detail::col::violet_red},
        {"VioletRed", detail::col::VioletRed},
        {"VioletRed1", detail::col::VioletRed1},
        {"VioletRed2", detail::col::VioletRed2},
        {"VioletRed3", detail::col::VioletRed3},
        {"VioletRed4", detail::col::VioletRed4},
        {"wheat", detail::col::wheat},
        {"wheat1", detail::col::wheat1},
        {"wheat2", detail::col::wheat2},
        {"wheat3", detail::col::wheat3},
        {"wheat4", detail::col::wheat4},
        {"white", detail::col::white},
        {"white smoke", detail::col::white_smoke},
        {"WhiteSmoke", detail::col::WhiteSmoke},
        {"yellow", detail::col::yellow},
        {"yellow green", detail::col::yellow_green},
        {"yellow1", detail::col::yellow1},
        {"yellow2", detail::col::yellow2},
        {"yellow3", detail::col::yellow3},
        {"yellow4", detail::col::yellow4},
        {"YellowGreen", detail::col::YellowGreen}
    };

    /**
     * Generates and returns a random color.
     * @return
     */
    inline Color randomColor() {
        static std::default_random_engine rng(detail::epochTime());
        static std::uniform_int_distribution<int> rng_dist(0, 255);

        return Color((uint8_t) rng_dist(rng), (uint8_t) rng_dist(rng), (uint8_t) rng_dist(rng));
    }

    /**\brief Retrieves a read-only reference to a color
     *         associated with the specified input name string.
     * Default colors have an associated name string you can use to retrieve
     * their values. All of the names can be found here:
     * https://www.tcl.tk/man/tcl8.4/TkCmd/colors.htm */
    inline Color fromName(const std::string& name) {
        return name == "random" ? randomColor() : Color(NAMED_COLORS.at(name));
    }

    //Define named color constructor after the definition of the named color map.

    /*\brief Name constructor.
                     Takes a literal color name as an input.
      \param name The name of the color from which to derive value.
      \sa fromName()*/
    Color::Color(const std::string& name) {
        const Color c = fromName(name);
        r = c.r;
        g = c.g;
        b = c.b;
    }

    //SECTION: USER IO

    /*Mouse event callback type.*/
    typedef std::function<void(int, int) > MouseFunc;

    /*Keyboard event callback type.*/
    typedef std::function<void() > KeyFunc;

    /*Timer event callback type.*/
    typedef std::function<void(void) > TimerFunc;

    /**\brief The KeyboardKey Enumeration contains declarations for all
     *        accepted keyboard input keys.
     * \see keyFromName()*/
    enum KeyboardKey {
        KEY_ESC = cimg_library::cimg::keyESC,
        KEY_F1 = cimg_library::cimg::keyF1,
        KEY_F2 = cimg_library::cimg::keyF2,
        KEY_F3 = cimg_library::cimg::keyF3,
        KEY_F4 = cimg_library::cimg::keyF4,
        KEY_F5 = cimg_library::cimg::keyF5,
        KEY_F6 = cimg_library::cimg::keyF6,
        KEY_F7 = cimg_library::cimg::keyF7,
        KEY_F8 = cimg_library::cimg::keyF8,
        KEY_F9 = cimg_library::cimg::keyF9,
        KEY_F10 = cimg_library::cimg::keyF10,
        KEY_F11 = cimg_library::cimg::keyF11,
        KEY_F12 = cimg_library::cimg::keyF12,
        KEY_PAUSE = cimg_library::cimg::keyPAUSE,
        KEY_1 = cimg_library::cimg::key1,
        KEY_2 = cimg_library::cimg::key2,
        KEY_3 = cimg_library::cimg::key3,
        KEY_4 = cimg_library::cimg::key4,
        KEY_5 = cimg_library::cimg::key5,
        KEY_6 = cimg_library::cimg::key6,
        KEY_7 = cimg_library::cimg::key7,
        KEY_8 = cimg_library::cimg::key8,
        KEY_9 = cimg_library::cimg::key9,
        KEY_0 = cimg_library::cimg::key0,
        KEY_BACKSPACE = cimg_library::cimg::keyBACKSPACE,
        KEY_INSERT = cimg_library::cimg::keyINSERT,
        KEY_HOME = cimg_library::cimg::keyHOME,
        KEY_PAGEUP = cimg_library::cimg::keyPAGEUP,
        KEY_TAB = cimg_library::cimg::keyTAB,
        KEY_Q = cimg_library::cimg::keyQ,
        KEY_W = cimg_library::cimg::keyW,
        KEY_E = cimg_library::cimg::keyE,
        KEY_R = cimg_library::cimg::keyR,
        KEY_T = cimg_library::cimg::keyT,
        KEY_Y = cimg_library::cimg::keyY,
        KEY_U = cimg_library::cimg::keyU,
        KEY_I = cimg_library::cimg::keyI,
        KEY_O = cimg_library::cimg::keyO,
        KEY_P = cimg_library::cimg::keyP,
        KEY_DELETE = cimg_library::cimg::keyDELETE,
        KEY_END = cimg_library::cimg::keyEND,
        KEY_PAGEDOWN = cimg_library::cimg::keyPAGEDOWN,
        KEY_CAPSLOCK = cimg_library::cimg::keyCAPSLOCK,
        KEY_A = cimg_library::cimg::keyA,
        KEY_S = cimg_library::cimg::keyS,
        KEY_D = cimg_library::cimg::keyD,
        KEY_F = cimg_library::cimg::keyF,
        KEY_G = cimg_library::cimg::keyG,
        KEY_H = cimg_library::cimg::keyH,
        KEY_J = cimg_library::cimg::keyJ,
        KEY_K = cimg_library::cimg::keyK,
        KEY_L = cimg_library::cimg::keyL,
        KEY_ENTER = cimg_library::cimg::keyENTER,
        KEY_SHIFTLEFT = cimg_library::cimg::keySHIFTLEFT,
        KEY_Z = cimg_library::cimg::keyZ,
        KEY_X = cimg_library::cimg::keyX,
        KEY_C = cimg_library::cimg::keyC,
        KEY_V = cimg_library::cimg::keyV,
        KEY_B = cimg_library::cimg::keyB,
        KEY_N = cimg_library::cimg::keyN,
        KEY_M = cimg_library::cimg::keyM,
        KEY_SHIFTRIGHT = cimg_library::cimg::keySHIFTRIGHT,
        KEY_ARROWUP = cimg_library::cimg::keyARROWUP,
        KEY_CTRLLEFT = cimg_library::cimg::keyCTRLLEFT,
        KEY_APPLEFT = cimg_library::cimg::keyAPPLEFT,
        KEY_ALT = cimg_library::cimg::keyALT,
        KEY_SPACE = cimg_library::cimg::keySPACE,
        KEY_ALTGR = cimg_library::cimg::keyALTGR,
        KEY_APPRIGHT = cimg_library::cimg::keyAPPRIGHT,
        KEY_MENU = cimg_library::cimg::keyMENU,
        KEY_CTRLRIGHT = cimg_library::cimg::keyCTRLRIGHT,
        KEY_ARROWLEFT = cimg_library::cimg::keyARROWLEFT,
        KEY_ARROWDOWN = cimg_library::cimg::keyARROWDOWN,
        KEY_ARROWRIGHT = cimg_library::cimg::keyARROWRIGHT,
        KEY_PAD0 = cimg_library::cimg::keyPAD0,
        KEY_PAD1 = cimg_library::cimg::keyPAD1,
        KEY_PAD2 = cimg_library::cimg::keyPAD2,
        KEY_PAD3 = cimg_library::cimg::keyPAD3,
        KEY_PAD4 = cimg_library::cimg::keyPAD4,
        KEY_PAD5 = cimg_library::cimg::keyPAD5,
        KEY_PAD6 = cimg_library::cimg::keyPAD6,
        KEY_PAD7 = cimg_library::cimg::keyPAD7,
        KEY_PAD8 = cimg_library::cimg::keyPAD8,
        KEY_PAD9 = cimg_library::cimg::keyPAD9,
        KEY_PADADD = cimg_library::cimg::keyPADADD,
        KEY_PADSUB = cimg_library::cimg::keyPADSUB,
        KEY_PADMUL = cimg_library::cimg::keyPADMUL,
        KEY_PADDIV = cimg_library::cimg::keyPADDIV
    };

    const std::unordered_map<std::string, KeyboardKey> NAMED_KEYS = {
        {"ESC", KEY_ESC},
        {"F1", KEY_F1},
        {"F2", KEY_F2},
        {"F3", KEY_F3},
        {"F4", KEY_F4},
        {"F5", KEY_F5},
        {"F6", KEY_F6},
        {"F7", KEY_F7},
        {"F8", KEY_F8},
        {"F9", KEY_F9},
        {"F10", KEY_F10},
        {"F11", KEY_F11},
        {"F12", KEY_F12},
        {"PAUSE", KEY_PAUSE},
        {"1", KEY_1},
        {"2", KEY_2},
        {"3", KEY_3},
        {"4", KEY_4},
        {"5", KEY_5},
        {"6", KEY_6},
        {"7", KEY_7},
        {"8", KEY_8},
        {"9", KEY_9},
        {"0", KEY_0},
        {"BACKSPACE", KEY_BACKSPACE},
        {"INSERT", KEY_INSERT},
        {"HOME", KEY_HOME},
        {"PAGEUP", KEY_PAGEUP},
        {"TAB", KEY_TAB},
        {"Q", KEY_Q},
        {"W", KEY_W},
        {"E", KEY_E},
        {"R", KEY_R},
        {"T", KEY_T},
        {"Y", KEY_Y},
        {"U", KEY_U},
        {"I", KEY_I},
        {"O", KEY_O},
        {"P", KEY_P},
        {"DELETE", KEY_DELETE},
        {"END", KEY_END},
        {"PAGEDOWN", KEY_PAGEDOWN},
        {"CAPSLOCK", KEY_CAPSLOCK},
        {"A", KEY_A},
        {"S", KEY_S},
        {"D", KEY_D},
        {"F", KEY_F},
        {"G", KEY_G},
        {"H", KEY_H},
        {"J", KEY_J},
        {"K", KEY_K},
        {"L", KEY_L},
        {"ENTER", KEY_ENTER},
        {"SHIFTLEFT", KEY_SHIFTLEFT},
        {"Z", KEY_Z},
        {"X", KEY_X},
        {"C", KEY_C},
        {"V", KEY_V},
        {"B", KEY_B},
        {"N", KEY_N},
        {"M", KEY_M},
        {"SHIFTRIGHT", KEY_SHIFTRIGHT},
        {"ARROWUP", KEY_ARROWUP},
        {"CTRLLEFT", KEY_CTRLLEFT},
        {"APPLEFT", KEY_APPLEFT},
        {"ALT", KEY_ALT},
        {"SPACE", KEY_SPACE},
        {"ALTGR", KEY_ALTGR},
        {"APPRIGHT", KEY_APPRIGHT},
        {"MENU", KEY_MENU},
        {"CTRLRIGHT", KEY_CTRLRIGHT},
        {"ARROWLEFT", KEY_ARROWLEFT},
        {"ARROWDOWN", KEY_ARROWDOWN},
        {"ARROWRIGHT", KEY_ARROWRIGHT},
        {"PAD0", KEY_PAD0},
        {"PAD1", KEY_PAD1},
        {"PAD2", KEY_PAD2},
        {"PAD3", KEY_PAD3},
        {"PAD4", KEY_PAD4},
        {"PAD5", KEY_PAD5},
        {"PAD6", KEY_PAD6},
        {"PAD7", KEY_PAD7},
        {"PAD8", KEY_PAD8},
        {"PAD9", KEY_PAD9},
        {"PADADD", KEY_PADADD},
        {"PADSUB", KEY_PADSUB},
        {"PADMUL", KEY_PADMUL},
        {"PADDIV", KEY_PADDIV}
    };

    /**\brief The MouseButton Enumeration holds all accepted mouse
     *        input buttons.
     *  These button enumerations are represented as bitwise flags.*/
    enum MouseButton {//Stored as bitwise flags from CImgDisplay
        MOUSEB_LEFT, //Left Mouse Button
        MOUSEB_RIGHT, //Right Mouse Button
        MOUSEB_MIDDLE//Middle Mouse Button
    };

    struct InputEvent {
        //True for keyboard, false for mouse
        bool type = false;
        //For keyboard; true if key down, false if key up.
        bool isDown = false;
        //mouseX, mouseY
        int mX = 0;
        int mY = 0;
        /*void callback pointer. cast and called when processed.*/
        void* cbPointer = nullptr;
    };

    /**
     * Returns a keyboard key enumeration when given its name as a string.
     * @param name
     * @return
     */
    inline KeyboardKey keyFromName(const std::string& name) {
        return NAMED_KEYS.at(name);
    }

    //SECTION: GEOMETRY (AND A LIL' BIT OF WHAT USED TO BE IN THE COMMON HEADER)

    /**\brief Represents a coordinate pair (e.g, x & y)
     * This class is represented as a low-precision point, because
     * this data type tends to be most easily drawn to a simple canvas.*/
    struct ivec2 {
        /**The X component.*/
        int x;
        /**The Y component.*/
        int y;

        /**\brief Empty constructor. Initializes X and Y to both equal 0.*/
        ivec2() : x(0), y(0){}

        /**\brief Assignment cons tructor.
         *\param x The X value of this ivec2.
         *\param y The Y value of this ivec2.*/
        ivec2(int x, int y) : x(x), y(y) {}

        /*Array access operator overload.*/

        /**\brief Array access operator overload. Useful for convenience.
         *\param index The index of one of the components of this ivec2 (0..1)
         *\return A reference to the index */
        inline int& operator[](int index){
            return index == 0 ? x : y;
        }

        /**\brief Array access operator overload. Useful for convenience.
         *\param index The index of one of the components of this ivec2 (0..1)
         *\return A reference to the index */
        inline int operator[](int index) const{
            return index == 0 ? x : y;
        }
        
        ivec2 operator+(const ivec2& other) const{
            return {x + other.x, y + other.y};
        }
        
        ivec2& operator+=(const ivec2& other){
            x += other.x;
            y += other.y;
            return *this;
        }
        
        ivec2 operator-(const ivec2& other) const{
            return {x - other.x, y - other.y};
        }

        ivec2& operator-=(const ivec2& other){
            x -= other.x;
            y -= other.y;
            return *this;
        }

        /**\brief Comparison operator between this vector and the other specified.*/
        bool operator==(const ivec2& other){
            return x == other.x && y == other.y;
        }
    };

    /**\brief Returns the distance between the two specified points.
     *\param a The first point.
     *\param b The second point.
     *\return The distance, in nondescript units, between the first and second points.*/
    inline int distance(const ivec2& a, const ivec2& b) {
        return static_cast<int>(std::sqrt(std::pow(b.x - a.x, 2) + std::pow(b.y - a.y, 2)));
    }

    /**\brief Finds the point that lies in the middle of the two specified.
     *\param a The first point.
     *\param b The second point.
     *\return The point between the first and second points.*/
    inline ivec2 middle(const ivec2& a, const ivec2& b) {
        return ivec2((a.x + b.x) / 2, (a.y + b.y) / 2);
    }

    /**\brief An alias for ivec2. Strictly for convenience and clarity.*/
    typedef ivec2 Point;

    /**\brief Draws a line of variable thickness on the specified image.
     * This needed to be implemented because the CImg display backend
     * has no facility to draw lines with a width greater than a single pixel!
     *\param imgRef The image on which to draw the line.
     *\param The X component of the first coordinate.
     *\param The Y component of the first coordinate.
     *\param the X component of the second coordinate.
     *\param the Y component of the second coordinate.
     *\param c The color with which to draw the line.
     *\param width The width of the line.*/
    inline void drawLine(Image& imgRef, int x1, int y1, int x2, int y2, Color c, unsigned int width = 1) {
        if(x1 == x2 && y1 == y2)
            return;
        else if (width == 1) {
            //Just use the built-in bresenham line function
            //to draw line with widths of 1.
            imgRef.draw_line(x1, y1, x2, y2, c.rgbPtr());
            return;
        }

        //We pretty much re-implement Bresenham's Line Algorithm here,
        //however instead of blitting pixels at each spot we put circles,
        //which matches the rounded thick lines present in the Python implementation.
        //This also allows for variable width.
        //Regrettably, this can be rather slow, but the invalidation
        //algorithm lessens how many times this has to be done for a given scene.

        const bool isSteep = (std::abs(y2 - y1) > std::abs(x2 - x1));
        if (isSteep) {
            std::swap(x1, y1);
            std::swap(x2, y2);
        }

        if (x1 > x2) {
            std::swap(x1, x2);
            std::swap(y1, y2);
        }

        const int dx = x2 - x1;
        const int dy = std::abs(y2 - y1);

        int err = dx / 2;
        const int ystep = (y1 < y2) ? 1 : -1;
        int y = y1;

        const int maxX = x2;
        const int radius = static_cast<int>(std::ceil(float(width) / 2.0f));
        for (int x = x1; x < maxX; x++) {
            if (isSteep){
                imgRef.draw_circle(y, x, radius, c.rgbPtr());
            }else{
                imgRef.draw_circle(x, y, radius, c.rgbPtr());
            }
            err -= dy;
            if (err < 0) {
                y += ystep;
                err += dx;
            }
        }
    }

    /**\brief The Transform class provides a myriad of functions to
     *        simply transform points.
     * This class it the backbone of almost all cartesian plane math in CTurtle.
     * An adapted 3x3 matrix of the following link:
     * http://www.opengl-tutorial.org/beginners-tutorials/tutorial-3-matrices/
     */
    class Transform {
    public:

        /**Constructs an empty transform.
         * Initializes, by default, as an identity transform.*/
        Transform() {
            identity();
        }

        /**\brief Copy constructor.
         *\param other The other transform from which to derive value.*/
        Transform(const Transform& other)
        : value(other.value), rotation(other.rotation) {
        }

        /**\brief Sets this transform to an identity.
         * When you concatenate an identity transform onto another object,
         * The resulting point is the same as it would have been pre-concatenation.
         * Such is the point of an identity transform, and is why Transforms
         * are initialized to have this value.
         *\return A reference to this transform. (e.g, *this)*/
        Transform& identity() {
            value.fill(0.0f);
            at(0, 0) = at(1, 1) = 1.0f;
            rotation = 0;
            return *this;
        }

        /**\brief Returns a boolean indicating if this transform
         *        is equivalent in value to the one specified.*/
        bool operator==(const Transform& other) const {
            bool eq = true;
            for (int i = 0; i < 9; i++) {
                if (value[i] != other.value[i]) {
                    eq = false;
                    break;
                }
            }
            return eq;
        }

        /**\brief Returns the X scale of this transform.
         *\return Returns the X scale of this transform.*/
        float getScaleX() const {
            return at(0, 0);
        }

        /**\brief Returns the Y scale of this transform.
         *\return Returns the Y scale of this transform.*/
        float getScaleY() const {
            return at(1, 1);
        }

        /**\brief Returns the X translation of this transform.
         *\return Returns the X translation of this transform.*/
        float getTranslateX() const {
            return at(0, 2);
        }

        /**\brief Returns the Y translation of this transform.
         *\return Returns the Y translation of this transform.*/
        float getTranslateY() const {
            return at(1, 2);
        }

        /**\brief Returns rotation of this transform, in radians.
         *\return The rotation of this transform, in radians.*/
        float getRotation() const {
            return rotation;
        }

        /**Moves this transform "forward" according to its rotation.*/
        Transform& forward(float distance) {
            //Adding the round here fixed rounding issues!
            at(0, 2) += std::round(std::cos(rotation) * distance); //x component
            at(1, 2) += std::round(std::sin(rotation) * distance); //y component
            return *this;
        }

        /*Backwards inline function.
          Just negates the input of a forward function call.*/
        inline Transform& backward(float distance) {
            return forward(-distance);
        }

        /**\brief Sets the translation of this transform.
         *\param x The number of units, or pixels, to transform on the X axis.
         *\param y The number of units, or pixels, to transform on the Y axis.
         *\return A reference to this transform. (e.g, *this)*/
        Transform& setTranslation(int x, int y) {
            at(0, 2) = static_cast<float>(x);
            at(1, 2) = static_cast<float>(y);
            return *this;
        }

        /**\brief Returns the translation of this transform as a point.
         *\return The point which represents the transform.*/
        Point getTranslation() const {
            return Point((int) at(0, 2), (int) at(1, 2));
        }

        /**\brief Sets the X axis translation of this transform.
         *\param x The number of units, or pixels, to transform on the X axis.
         *\return A reference to this transform. (e.g, *this)*/
        Transform& setTranslationX(int x) {
            at(0, 2) = static_cast<float>(x);
            return *this;
        }

        /**\brief Set the Y axis translation of this transform.
         *\param y The number of units, or pixels, to transform on the Y axis.
         *\return A reference to this transform. (e.g, *this)*/
        Transform& setTranslationY(int y) {
            at(1, 2) = static_cast<float>(y);
            return *this;
        }

        /**\brief Translates this transform.
         *\param x The number of units, or pixels, to transform on the X axis.
         *\param y The number of units, or pixels, to transform on the Y axis.
         *\return A reference to this transform. (e.g, *this)*/
        Transform& translate(int x, int y) {
            at(0, 2) += static_cast<float>(x) * at(0, 0) + static_cast<float>(y) * at(0, 1);
            at(1, 2) += static_cast<float>(x) * at(1, 0) + static_cast<float>(y) * at(1, 1);
            return *this;
        }

        /**\brief Rotates this transform.
         *\param theta The angle at which to rotate, in radians
         *\return A reference to this transform. (e.g, *this)*/
        Transform& rotate(float theta) {
            //6.28319 is a full rotation in radians. (360 degrees)
            constexpr float fullcircle = 6.28319f;

            //Much smarter solution than recursive spinning.
            //Takes the modulus between what would have been the pre-fix result
            //and a full circle, and subtracts the original rotation.
            //This gives pretty accurate rotations rather quickly.
            //No recursive spinning required! :)
            const float origResult = rotation + theta;
            if (origResult > fullcircle || origResult < 0) 
                theta = std::fmod(origResult, fullcircle) - rotation;

            const float c = std::cos(theta);
            const float s = std::sin(theta);

            const float new00 = at(0, 0) * c + at(0, 1) * s;
            const float new01 = at(0, 0) * -s + at(0, 1) * c;
            const float new10 = at(1, 0) * c + at(1, 1) * s;
            const float new11 = at(1, 0) * -s + at(1, 1) * c;

            at(0, 0) = new00;//x
            at(0, 1) = new01;//y
            at(1, 0) = new10;//rotX
            at(1, 1) = new11;//rotY

            rotation += theta;

            return *this;
        }

        /**\brief Sets the rotation of this transform.
         *\param val The angle at which to rotate, in radians.
         *\return A reference to this transform. (e.g, *this)*/
        Transform& setRotation(float val) {
            if (val == rotation)
                return *this;
            if (rotation != 0.0f)
                rotate(-rotation);
            rotate(val);
            return *this;
        }

        /**\brief Rotates this transform around a specified point.
         *\param x The X coordinate to rotate around.
         *\param y The Y coordinate to rotate around.
         *\param theta The angle at which to rotate, in radians
         *\return A reference to this transform. (e.g, *this)*/
        Transform& rotateAround(int x, int y, float theta) {
            translate(x, y);
            rotate(theta);
            translate(-x, -y);
            return *this;
        }

        /**\brief Applies a scale transformation to this transform.
         *\param sx The X axis scale factor.
         *\param sy The Y axis scale factor.*/
        Transform& scale(float sx, float sy) {
            at(0, 0) *= sx;
            at(0, 1) *= sy;
            at(1, 0) *= sx;
            at(1, 1) *= sy;
            return *this;
        }

        /**\brief Concatenates this Transform with another.
         *\param t The other Transform to concatenate with.
         *\return A reference to this transform. (e.g, *this)*/
        Transform& concatenate(const Transform& t) {
            const float new00 = at(0, 0) * t.at(0, 0) + at(0, 1) * t.at(1, 0);
            const float new01 = at(0, 0) * t.at(0, 1) + at(0, 1) * t.at(1, 1);
            const float new02 = at(0, 0) * t.at(0, 2) + at(0, 1) * t.at(1, 2) + at(0, 2);
            const float new10 = at(1, 0) * t.at(0, 0) + at(1, 1) * t.at(1, 0);
            const float new11 = at(1, 0) * t.at(0, 1) + at(1, 1) * t.at(1, 1);
            const float new12 = at(1, 0) * t.at(0, 2) + at(1, 1) * t.at(1, 2) + at(1, 2);

            at(0, 0) = new00;
            at(0, 1) = new01;
            at(0, 2) = new02;
            at(1, 0) = new10;
            at(1, 1) = new11;
            at(1, 2) = new12;
            rotation += t.rotation;
            return *this;
        }

        /**\brief Creates a copy of this transform, concatenates the input, and returns it.
         *\param t The input to concatenate onto the copy of this transform.
         *\return Returns the concatenated copy of this transform.*/
        Transform copyConcatenate(const Transform& t) const {
            Transform copy;
            copy.assign(*this);
            copy.concatenate(t);
            return copy;
        }

        /**\brief Interpolates between this and the specified transform.
         *        Progress is a float in range of 0 to 1.
         *\param t The destination transform.
         *\param progress A progress float in range of 0 to 1.
         *\return The resulting interpolated transform.*/
        Transform lerp(const Transform& t, float progress) const {
            if (progress <= 0)
                return *this;
            else if (progress >= 1)
                return t;
            Transform result;
            for (int i = 0; i < 9; i++) {
                result.value[i] = (progress * (t.value[i] - value[i])) + value[i];
            }
            return result;
        }

        /**\brief Assigns the value of this transform to that of another.
         *\param t The other transform to derive value from.*/
        void assign(const Transform& t) {
            value = t.value;
            rotation = t.rotation;
        }

        /**\brief Transforms a point according to this transform.
         *\param in The input point.
         *\param dst The destination pointer to store the value. Can be same as input..
         *\return Returns the translated point.
         *\return Also assigns the value of dst pointer to the result.*/
        Point transform(Point in, Point* dst = nullptr) const {
            Point temp;
            Point* dstPtr = (dst == nullptr) ? &temp : dst;

            dstPtr->x = static_cast<int>(
                        at(0, 0) * (static_cast<float>(in.x)) +
                        at(0, 1) * (static_cast<float>(in.y)) + at(0, 2));
            dstPtr->y = static_cast<int>(
                        at(1, 0) * (static_cast<float>(in.x)) +
                        at(1, 1) * (static_cast<float>(in.y)) + at(1, 2));
            
            return *dstPtr;
        }

        /**\brief Transforms a set of points given a begin and end iterator.
         *\param cur The beginning iterator of a set.
         *\param end The ending iterator of a set.*/
        template<typename ITER_T>
        void transformSet(ITER_T cur, ITER_T end) const {
            while (cur != end) {
                transform(&(*cur), &(*cur));
                cur++;
            }
        }

        /*Operator overload to transform a single point, for convenience.*/

        /**\brief Operator overload to transform a single point.
         *\param in The point to transform.*/
        inline Point operator()(Point in) const {
            return transform(in);
        }
    protected:
        /**The underlying matrix type.
         * It's defined simply as an array of 9 floats.
         * Retrieved from coordinate pairs using (x*3+y) as indices.*/
        typedef std::array<float, 9> mat_t;

        /**The value of this transform.*/
        mat_t value;

        /**The rotation of this transform, in radians.*/
        float rotation = 0;

        /**\brief Returns a reference to the float the specified coordinate.
         *\param row The specified row from which to get a component.
         *\param col The specified column from which to get a component.*/
        inline float& at(int row, int col) {
            return value[row * 3 + col];
        }

        /**\brief Returns a copy of the float at the specified coordinate.
         *\param row The specified row from which to get a component.
         *\param col The specified column from which to get a component.*/
        float at(int row, int col) const {
            return value[row * 3 + col];
        }
    };

    /**\brief Converts degrees to radians.
     * A generic toRadians function. Performs
     * the following: val*(PI/180.0)
     * \param val The value to convert from degress to radians.
     * \return A value of the same type as val, converted to radians.*/
    template<typename T>
    inline T toRadians(T val) {
        return T(val * (M_PI / 180.0));
    }

    /**\brief Converts radians to degrees.
     * A generic toDegrees function. Performs
     * the following: val*(180.0/PI)
     * \param val The value to convert from radians to degrees.
     * \return A value of the same type as val, converted to degrees.*/
    template<typename T>
    inline T toDegrees(T val) {
        return std::round(T(val * (180.0 / M_PI)));
    }

    /**\brief AbstractDrawableObject is a base class, intended to be
     *        inherited from by all drawable objects.
     * This class just contains a simple virtual drawing function,
     * intended to be inherited from and to overload the draw function.
     * This allows for the storage of drawable geometry/etc and attributes in a generic fashion.*/
    class AbstractDrawableObject {
    public:

        /**The internal fill color of the circle.*/
        Color fillColor;

        /**The outline color of the circle.*/
        Color outlineColor;

        /**The width of the outline of the circle, in pixels.*/
        int outlineWidth = 0;

        /**\brief Empty default constructor.*/
        AbstractDrawableObject() {
        }

        /**\brief Empty-- virtual-- default de-constructor.*/
        virtual ~AbstractDrawableObject() {
        }

        /**\brief Returns a pointer to a copy of this drawable object, allocated with NEW.
         * Result Must be deleted at the responsibility of the invoker.*/
        virtual AbstractDrawableObject* copy() const = 0;

        /**\brief This function is intended to draw all applicable geometry
         *        in this object to the specified image, with the specified transform,
         *        with the specified color.
         * This function is intended to be overloaded by child classes to draw applicable
         * geometry to an image, acting as a canvas.
         * \param t The transform at which to draw the geometry.
         * \param imgRef The canvas on which to draw.
         * \param c The color with to draw the geometry.*/
        virtual void draw(const Transform& t, Image& imgRef) const = 0;
    };

    class Text : public AbstractDrawableObject {
    public:
        /** The text to draw.*/
        std::string text;

        /**Blank default destructor.*/
        Text(){}

        Text(const std::string& text, Color color)
            : text(text){
            fillColor = color;
        }

        Text(const Text& copy)
            : text(copy.text){
            fillColor = copy.fillColor;
        }

        AbstractDrawableObject* copy() const{
            return new Text(*this);
        }

        void draw(const Transform& t, Image& imgRef) const{
            const Point pos = t.getTranslation();
            imgRef.draw_text(pos.x,pos.y,text.c_str(),fillColor.rgbPtr());
        }

        ~Text(){}
    };

    /**\brief The Line class holds two points and the functionality to draw a line
     *       between them on a specified canvas.*/
    class Line : public AbstractDrawableObject {
    public:
        /**The "From" point.
           Lines drawn with this object start here.*/
        Point pointA;
        /**The "To" point.
           Lines drawn with this object end here.*/
        Point pointB;

        /**The width of the line, in pixels.*/
        int width = 1;

        /**\brief Empty default constructor.*/
        Line() {}

        /**\brief Value constructor.
         *        merely assigns value of pointA and pointB to respective A and B.
         *\param a The "From" point.
         *\param b The "To" point.*/
        Line(Point a, Point b, Color color, int width = 1) : pointA(a), pointB(b), width(width){
            fillColor = color;
        }

        /**\brief Copy constructor.
         *        Merely assigns the "to" and "from" points.
         *\param other The other instance of a line from which to derive value.*/
        Line(const Line& other) : pointA(other.pointA), pointB(other.pointB), width(other.width) {
            fillColor = other.fillColor;
        }

        AbstractDrawableObject* copy() const{
            return new Line(*this);
        }

        /**\brief Empty de-constructor.*/
        ~Line() {
        }

        void draw(const Transform& t, Image& imgRef) const{
            const Point a = t(pointA);
            const Point b = t(pointB);
            drawLine(imgRef, a.x, a.y, b.x, b.y, fillColor, width);
        }
    };

    /**\brief The Circle class holds a radius and total number of steps, used
     *        to generate and draw a circles geometry.*/
    class Circle : public AbstractDrawableObject {
    public:
        /**Radius, in pixels, of the geometry generated in the draw function.*/
        int radius = 10;
        /**Total number of steps, or vertices, generated in the draw function.
         * The higher this number is, the more "high-quality" it can be considered.*/
        int steps = 10;

        /**\brief Empty constructor.*/
        Circle() {
        }

        /**\brief Radius and step assignment constructor.
         *\param radius The radius, in pixels, of this circle.
         *\param steps The number of vertices used by this circle.*/
        Circle(int radius, int steps, Color fillColor, int outlineWidth = 0, Color outlineColor = Color())
            : radius(radius), steps(steps){
            this->fillColor = fillColor;
            this->outlineWidth = outlineWidth;
            this->outlineColor = outlineColor;
        }

        /**\brief Copy constructor.
         *\param other Another instance of a circle from which to derive value.*/
        Circle(const Circle& other)
            : radius(other.radius), steps(other.steps){
            this->fillColor = fillColor;
            this->outlineWidth = outlineWidth;
            this->outlineColor = outlineColor;
        }

        AbstractDrawableObject* copy() const{
            return new Circle(*this);
        }

        void draw(const Transform& t, Image& imgRef) const{
            if (steps <= 0)
                return; //no step check
            cimg::CImg<int> passPts(steps, 2);

            for (int i = 0; i < steps; i++) {
                Point p;
                p.x = int(radius * std::cos(i * (2 * M_PI) / steps));
                p.y = int(radius * std::sin(i * (2 * M_PI) / steps));
                Point tPoint = t(p);
                passPts(i, 0) = tPoint.x;
                passPts(i, 1) = tPoint.y;
            }

            imgRef.draw_polygon(passPts, fillColor.rgbPtr());

            if (outlineWidth > 0) {//draw outline using previously generated points.
                //LineLoop impl
                for (int i = 1; i < steps; i++) {
                    drawLine(imgRef, passPts(i - 1, 0), passPts(i - 1, 1), passPts(i, 0), passPts(i, 1), outlineColor, outlineWidth);
                }
                //draw last line between first and last
                drawLine(imgRef, passPts(steps - 1, 0), passPts(steps - 1, 1), passPts(0, 0), passPts(0, 1), outlineColor, outlineWidth);
            }
        }
    };

    /**\brief The polygon class merely holds a vector of points and a function
     *        to draw this series to an image.
     * Please note that the contained series of points must be in either
     * clockwise(CW) or counterclockwise(CCW) order!*/
    class Polygon : public AbstractDrawableObject {
    public:
        std::vector<Point> points;

        /**\brief Empty default constructor.*/
        Polygon() {
        }

        /**\brief   Initializer list instructor which assigns the points
         *          to the contents of the specified initializer list.
         *\param The initializer list from where points are retrieved.*/
        Polygon(const std::initializer_list<Point>& init)
             : points(init){
            this->outlineWidth = outlineWidth;
            this->outlineColor = outlineColor;
            this->fillColor = fillColor;
        }

        /**\brief A copy constructor for another vector of points.
         *\param copy A vector from which to derive points.*/
        Polygon(const std::vector<Point>& copy, Color fillColor, int outlineWidth = 0, Color outlineColor = Color())
             : points(copy){
            this->outlineWidth = outlineWidth;
            this->outlineColor = outlineColor;
            this->fillColor = fillColor;
        }

        /**\brief A copy constructor for another polygon.
         *\param other Another polygon from which to derive points.*/
        Polygon(const Polygon& other) {
            points = other.points;
            fillColor = other.fillColor;
            outlineColor = other.outlineColor;
            outlineWidth = other.outlineWidth;
        }

        AbstractDrawableObject* copy() const{
            return new Polygon(*this);
        }

        /**\brief Empty de-constructor.*/
        ~Polygon() {
        }

        void draw(const Transform& t, Image& imgRef) const{
            if (points.empty())
                return;
            /*CImg is a pain in the butt and requires all polygons to be
              passed in as an instance of the image object. Therefore,
              we can specify an "int" image with a width of 2 (x,y) and height
              of the total number of elements in the point vector.*/
            cimg::CImg<int> passPts(static_cast<int>(points.size()), 2);

            for (int i = 0; i < points.size(); i++) {
                const Point pt = t(points[i]);
                passPts(i, 0) = pt.x;
                passPts(i, 1) = pt.y;
            }

            imgRef.draw_polygon(passPts, fillColor.rgbPtr());

            if (outlineWidth > 0) {//draw outline using previously generated points.
                //LineLoop impl
                for (int i = 1; i < points.size(); i++) {
                    drawLine(imgRef, passPts(i - 1, 0), passPts(i - 1, 1), passPts(i, 0), passPts(i, 1), outlineColor, outlineWidth);
                }
                //draw last line between first and last
                drawLine(imgRef, passPts(int(points.size()) - 1, 0), passPts(int(points.size()) - 1, 1), passPts(0, 0), passPts(0, 1), outlineColor, outlineWidth);
            }
        }
    };

    /**
     * Sprites represent a selection of an image.*/
    class Sprite : public AbstractDrawableObject {
    public:
        int srcX, srcY, srcW, srcH;

        int drawWidth = 0;
        int drawHeight = 0;

        Sprite(Image& img, int outlineWidth = 0, Color outlineColor = Color()) : spriteImg(img) {
            srcX = srcY = 0;
            srcW = img.width();
            srcH = img.height();
        }

        Sprite(Image& img, int srcX, int srcY, int srcW, int srcH, int outlineWidth = 0, Color outlineColor = Color()) : spriteImg(img) {
            this->srcX = srcX;
            this->srcY = srcY;
            this->srcW = srcW;
            this->srcH = srcH;
            this->outlineWidth = outlineWidth;
            this->outlineColor = outlineColor;
        }

        Sprite(const Sprite& copy) : spriteImg(copy.spriteImg) {
            this->srcX = copy.srcX;
            this->srcY = copy.srcY;
            this->srcW = copy.srcW;
            this->srcH = copy.srcH;
            this->drawWidth = copy.drawWidth;
            this->drawHeight = copy.drawHeight;
            this->outlineWidth = outlineWidth;
            this->outlineColor = outlineColor;
        }

        ~Sprite() {
        }

        AbstractDrawableObject* copy() const{
            return new Sprite(*this);
        }

        /**Draws this Sprite.
         * Disregards the Color attribute in favor of sprites colors.*/
        void draw(const Transform& t, Image& imgRef) const {
            //Vertex order is as follows for the constructed quad.
            // 0--3   3
            // | /   /|
            // |/   / |
            // 1   1--2

            const int halfW = drawWidth / 2;
            const int halfH = drawHeight / 2;

            Point destPoints[4] = {
                {-halfW, halfH}, //0
                {-halfW, -halfH}, //1
                {halfW, -halfH}, //2
                {halfW, halfH} //3
            };

            Point texturePoints[4] = {
                {srcX, srcY},
                {srcX, srcY + srcH},
                {srcX + srcW, srcY},
                {srcX + srcW, srcY + srcH}
            };

            /**Transforms the set of destination points.*/
            for (int i = 0; i < 4; i++) {
                destPoints[i] = t(destPoints[i]);
            }

            //Yes, I know this isn't particularly readable.
            //But its purpose is described in an above commented illustration.
            imgRef.draw_triangle(destPoints[0][0], destPoints[0][1], destPoints[1][0], destPoints[1][1], destPoints[3][0], destPoints[3][1],
                    spriteImg, texturePoints[0][0], texturePoints[0][1], texturePoints[1][0], texturePoints[1][1], texturePoints[3][0], texturePoints[3][1]);
            imgRef.draw_triangle(destPoints[1][0], destPoints[1][1], destPoints[2][0], destPoints[2][1], destPoints[3][0], destPoints[3][1],
                    spriteImg, texturePoints[1][0], texturePoints[1][1], texturePoints[2][0], texturePoints[2][1], texturePoints[3][0], texturePoints[3][1]);

            if (outlineWidth > 0) {//draw outline using previously generated points.
                //LineLoop impl
                for (int i = 1; i < 4; i++) {
                    drawLine(imgRef, destPoints[i - 1][0], destPoints[i - 1][1], destPoints[i][0], destPoints[i][1], outlineColor, outlineWidth);
                }
                //draw last line between first and last
                drawLine(imgRef, destPoints[3][0], destPoints[3][1], destPoints[0][0], destPoints[0][1], outlineColor, outlineWidth);
            }
        }
    protected:
        Image& spriteImg;
    };

    /**
     * Compound Polygons can have a variety of attachments.
     * */
    class CompoundPolygon : public AbstractDrawableObject {
    public:
        typedef std::pair<Transform, std::unique_ptr<AbstractDrawableObject>> component_t;

        CompoundPolygon() {
        }

        CompoundPolygon(const CompoundPolygon& copy){
            for(const component_t& component : copy.components){
                components.emplace_back(component.first, component.second->copy());
            }
        }

        /**Adds a generic component to this CompoundPolygon.*/
        void addcomponent(const AbstractDrawableObject& obj, const Transform& transform = Transform()) {
            components.emplace_back(transform, obj.copy());
        }

        AbstractDrawableObject* copy() const{
            return new CompoundPolygon(*this);
        }

        /**Draws this CompoundPolygon.
         * Disregards the Color attribute in favor of the components' colors*/
        void draw(const Transform& t, Image& imgRef) const{
            for (const component_t& comp : components) {
                comp.second->draw(t.copyConcatenate(comp.first), imgRef);
            }
        }
    protected:
        std::list<component_t> components;
    };

    //SECTION: TURTLE & TURTLE SCREEN

    //Turtle prototype definition
    class Turtle;
    //TurtleScreen prototype definition
    class InteractiveTurtleScreen;

    /**\brief Describes the speed at which a Turtle moves and rotates.
     * \sa Turtle::getAnimMS()*/
    enum TurtleSpeed {
        /**So fast, it disables animation.*/
        TS_FASTEST = 0,
        /**The fastest the turtle can go without disabling animations.*/
        TS_FAST = 10,
        /**The default, normal speed of a turtle.*/
        TS_NORMAL = 6,
        /**A slow speed.*/
        TS_SLOW = 3,
        /**The slowest a turtle can go.*/
        TS_SLOWEST = 1
    };

    /**\brief Turtles append Scene Objects to a list to keep
     *              track of what it has drawn (a history).
     * SceneObject holds a description of something that needs to be on the screen.
     * It's a general object which encompasses ALL things that can be on screen,
     * ranging from stamps, misc. geometry, and strings.*/
    struct SceneObject {
        /**The unique pointer to the geometry of this object.
         * MUST BE NON-NULL IF THE OBJECT IS IN A TURTLE SCREEN'S SCENE.*/
        std::unique_ptr<AbstractDrawableObject> geom;

        /**The transform at which to draw this SceneObject.
         * Note that this is concatenated onto the ScreenTransform of
         * the drawing turtle's screen.*/
        Transform transform;

        /**A boolean indicating if this scene object is a stamp.*/
        bool stamp = false;
        /**The integer representing the stamp ID, if this is a stamp. Valid stampids > -1*/
        int stampid = -1;

        /**Empty constructor.*/
        SceneObject() {
        }

        /**General geometry constructor.
         *\param geom A dynamically allocated pointer to a Geometry object.
         *            Please note that, after this constructor call, the SceneObject
         *            controls the life of the given pointer. Do not delete it yourself.
         *\param color The color to draw the geometry in.
         *\param t The transform at which to draw the geometry.
         *\param stampid The ID of the stamp this object is related to.*/
        SceneObject(AbstractDrawableObject* geom, const Transform& t, int stampid = -1) :
                geom(geom), transform(t), stamp(stampid>-1), stampid(stampid) {
        }
    };

    /**Pen State structure.
     * Holds all pen attributes.*/
    struct PenState {
        /**The transform of the pen.
         * holds position, rotation, and scale of the turtle.*/
        Transform transform;
        /**The movement speed of the turtle, in range of 0...10*/
        float moveSpeed = TS_NORMAL;
        /**Whether or not the turtle's "tail" (or pen) is down.*/
        bool tracing = true;
        /**The angle mode. False for degrees, true for radians.*/
        bool angleMode = false;
        /**The width of the pen, in pixels.*/
        int penWidth = 1;
        /**A boolean indicating if we're trying to fill a shape.*/
        bool filling = false;
        /**The color of the pen.*/
        Color penColor = Color("black");
        /**The intended fill color.*/
        Color fillColor = Color("black");
        /**The total number of objects in the screen's object stack
         * prior to the addition of this state->*/
        size_t objectsBefore = 0;
        /**The turtle's cursor geometry. MUST ASSIGN BEFORE USE.*/
        std::unique_ptr<AbstractDrawableObject> cursor = nullptr;
        /**The current stamp ID.*/
        int curStamp = 0;
        /**A boolean indicating if this turtle is visible.*/
        bool visible = true;
        /**A float for cursor tilt (e.g, rotation appleid to the cursor itself)*/
        float cursorTilt = 0;

        PenState(){}
        PenState(const PenState& copy) {
            transform = copy.transform;
            moveSpeed = copy.moveSpeed;
            tracing = copy.tracing;
            angleMode = copy.angleMode;
            penWidth = copy.penWidth;
            filling = copy.filling;
            penColor = copy.penColor;
            fillColor = copy.fillColor;
            cursor.reset(copy.cursor.get() ? copy.cursor->copy() : nullptr);
            curStamp = copy.curStamp;
            visible = copy.visible;
            cursorTilt = copy.cursorTilt;
            objectsBefore = copy.objectsBefore;
        }

        PenState& operator=(const PenState& copy){
            transform = copy.transform;
            moveSpeed = copy.moveSpeed;
            tracing = copy.tracing;
            angleMode = copy.angleMode;
            penWidth = copy.penWidth;
            filling = copy.filling;
            penColor = copy.penColor;
            fillColor = copy.fillColor;
            cursor.reset(copy.cursor.get() ? copy.cursor->copy() : nullptr);
            curStamp = copy.curStamp;
            visible = copy.visible;
            cursorTilt = copy.cursorTilt;
            objectsBefore = copy.objectsBefore;
            return *this;
        }
    };

    /**\brief ScreenMode Enumeration, used to decide orientation of the drawing calls
     *        on TurtleScreens.
     *\sa TurtleScreen::mode(ScreenMode)*/
    enum ScreenMode {
        SM_STANDARD,
        SM_LOGO//,
        //        SM_WORLD
    };
    //I'm leaving out SM_WORLD. Adding it would really require more work than I have time for.

    //Turtle class prototype so we can go ahead and define abstract turtle screen type.
    class Turtle;

    /**
     * The AbstractTurtleScreen class is the abstract type
     * for most turtle functionality.
     * It intentionally excludes all input/output functionality, allowing
     * for two intended derivates: an "interactive" screen, vs an "offline rendering" screen.
     * Turtle class doesn't care which one it gets, in theory.
     */
    class AbstractTurtleScreen{
    public:
        virtual ~AbstractTurtleScreen() = default;

        virtual void tracer(int countmax, unsigned int delayMS = 10) = 0;

        virtual int window_width() const = 0;
        virtual int window_height() const = 0;
        virtual Color bgcolor() const = 0;
        virtual void bgcolor(const Color& c) = 0;
        virtual void mode(ScreenMode mode) = 0;
        virtual ScreenMode mode() const = 0;
        virtual void clearscreen() = 0;

        /**Alias for clearscreen function
         *\sa clearscreen()*/
        inline void clear() {
            clearscreen();
        }

        virtual void resetscreen() = 0;

        /**Resets all turtles belonging to this screen to their original state->*/
        inline void reset() {
            resetscreen();
        }

        /**
         * @return a boolean indicating if this turtle screen supports live animation.
         */
        virtual bool supports_live_animation() const = 0;

        virtual ivec2 screensize(Color& bg) = 0;
        //code-smell from python->c++, considering separation of functionality

        virtual ivec2 screensize() = 0;
        virtual void update(bool invalidateDraw = false, bool processInput = true) = 0;
        virtual void delay(unsigned int ms) = 0;
        virtual unsigned int delay() = 0;
        virtual void bye() = 0;

        virtual Image& getcanvas() = 0;

        virtual bool isclosed() = 0;

        virtual void redraw(bool invalidate = false) = 0;

        virtual Transform screentransform() const = 0;

        virtual void add(Turtle& turtle) = 0;

        virtual std::list<SceneObject>& getScene() = 0;

        virtual AbstractDrawableObject& shape(const std::string& name) = 0;
    protected:
        //Abstract class. Private constructor only allows
        //for derivative classes to be instantiated.
        AbstractTurtleScreen(){};
    };

    /**
     *  The Turtle Class
     * Symbolically represents a turtle that runs around a screen that has a
     * paint brush attached to its tail. The tail can be in two states; up and down.
     * As the turtle moves forwards, backwards, left, and right, it can draw
     * shapes and outlines, write text, and stamp itself onto whatever surface
     * it's walking/crawling on (In this case, it's walking on a TurtleScreen).
     *
     * \sa TurtleScreen
     */
    class Turtle {
    public:
        Turtle(AbstractTurtleScreen& scr);

        //Motion

        /**\brief Moves the turtle forward the specified number of pixels.*/
        void forward(int pixels);

        /**\copydoc forward(int)*/
        inline void fd(int pixels) {
            forward(pixels);
        }

        /**\brief Moves the turtle backward the specified number of pixels.*/
        void backward(int pixels);

        /**\copydoc backward(int)*/
        inline void bk(int pixels) {
            backward(pixels);
        }

        /**\copydoc backward(int)*/
        inline void back(int pixels) {
            backward(pixels);
        }

        /**\brief Rotates the turtle the specified number of units to the right.
         * The unit by which the input is specified is determined by the current
         * angle mode. The difference between Clockwise and Counterclockwise
         * is determined by the current screen's mode.
         * \sa degrees()
         * \sa radians()
         * \sa TurtleScreen::mode()*/
        void right(float amt);

        /**\copydoc right(float)*/
        inline void rt(float angle) {
            right(angle);
        }

        /**\brief Rotates the turtle the specified number of units to the left.
         * The unit by which the input is specified is determined by the current
         * angle mode. The difference between Clockwise and Counterclockwise
         * is determined by the current screen's mode.
         * \sa degrees()
         * \sa radians()
         * \sa TurtleScreen::mode()*/
        void left(float amt);

        /**\copydoc left(float)*/
        inline void lt(float angle) {
            left(angle);
        }

        /**\brief Sets the transform location of this turtle.*/
        void goTo(int x, int y);

        /**\brief Sets the transform location of this turtle.*/
        inline void goTo(const Point& pt){
            goTo(pt.x, pt.y);
        }

        /**\copydoc goTo(int,int)*/
        inline void setpos(int x, int y) {
            goTo(x, y);
        }

        /**\copydoc goTo(int,int)*/
        inline void setpos(const Point& pt){
            goTo(pt.x, pt.y);
        }

        /**\copydoc goTo(int,int)*/
        inline void setposition(int x, int y) {
            goTo(x, y);
        }

        /**\copydoc goTo(int,int)*/
        inline void setposition(const Point& pt){
            goTo(pt.x, pt.y);
        }

        /**\brief Sets the X-axis transform location of this turtle.*/
        void setx(int x);
        /**\brief Sets the Y-axis transform location of this turtle.*/
        void sety(int y);
        
        /**
         * Adds a "dumb" translation to the current turtle's transform.
         * Does not take into account the rotation, or orientation, of the turtle.
         * @param x component of coordinate pair
         * @param y component of coordinate pair.
         */
        void shift(int x, int y);
        
        /**
         * @return a constant reference to the current state of this turtle.
         */
        const PenState& penstate() const{
            return *state;
        }

        /**\brief Sets the rotation of this turtle.
         * The unit by which the input is specified is determined by the current
         * angle mode. The difference between Clockwise and Counterclockwise
         * is determined by the current screen's mode.
         * \sa degrees()
         * \sa radians()
         * \sa TurtleScreen::mode()*/
        void setheading(float angle);

        /**
         * Returns the distance between this turtle and the given coordinate pair.
         * @param x
         * @param y
         * @return
         */
        int distance(int x, int y){
            return cturtle::distance(transform->getTranslation(), {x,y});
        }

        /**
         * Returns the distance between this turtle and the given point.
         * @param pt
         * @return
         * \sa distance(int, int)
         */
        int distance(const Point& pt){
            return cturtle::distance(transform->getTranslation(), pt);
        }

        /**\copydoc setheading(float)*/
        inline void seth(float angle) {
            setheading(angle);
        }

        /**
         * \brief Returns the angle between the line of the current turtle transform to the given point.
         * @param x component of coordinate pair
         * @param y component of coordinate pair.
         * @return
         */
        float towards(int x, int y);

        /**
         * \brief Returns the angle between the line of the current turtle transform to the given point.
         * @param pt
         * @return
         */
        inline float towards(const Point& pt){
            return towards(pt.x, pt.y);
        }

        /**
         * Returns the heading of the Turtle (e.g, its current rotation).
         * @return
         */
        inline float heading() {
            return state->angleMode ? transform->getRotation() : toDegrees(transform->getRotation());
        }

        /**\Brings the turtle back to its origin.
         * Depends on the current screen mode.
         * If the screen mode is set to "world", The turtle is turned to the right and
         * positive angles are counterclockwise.
         * Otherwise, if it is set to "logo", The turtle face upwards and positive
         * angles are clockwise.
         * \sa TurtleScreen::mode()*/
        void home();

        /**\brief Adds a circle to the screen.
         *\param radius The radius, in pixels, of the circle.
         *\param steps The "quality" of the circle. Higher is slow but looks better.
         *\param color The color of the circle.*/
        void circle(int radius, int steps, Color color);

        /**\brief Adds a circle to the screen.
         * Default parameters are circle with a radius of 30 with 15 steps.
         *\param color The color of the circle.*/
        inline void circle(Color color) {
            circle(30, 15, color);
        }

        /**\brief Adds a dot to the screen.
         *\param The color of the dot.
         *\param size The size of the dot.
         */
        void dot(Color color, int size = 10) {
            circle(size / 2, 4, color);
        }

        /**\brief Sets the "filling" state->
         * If the input is false but the prior state is true, a SceneObject
         * is put on the screen in the shape of the previously captured points.
         *\param state Whether or not the turtle is filling a polygon.*/
        void fill(bool state);

        inline bool filling() const{
            return penstate().filling;
        }
        
        /**\brief Begins filling a polygon.
         *\sa fill(bool)*/
        inline void begin_fill() {
            fill(true);
        }

        /**\brief Stops filling a polygon.
         *\sa fill(bool)*/
        inline void end_fill() {
            fill(false);
        }

        /**\brief Sets the fill color of this turtle.
         *\param c The color with which to fill polygons.*/
        void fillcolor(Color c) {
            pushState();
            state->fillColor = c;
            updateParent(false, false);
        }

        /**\brief Returns the fill color of this turtle.
         *\return The current fill color.*/
        Color fillcolor() {
            return state->fillColor;
        }

        /**Writes the specified string to the screen.
         * Uses the current filling color.
         *\param text The text to write.
         *\sa fillcolor(color)*/
        void write(const std::string& text);

        /**Writes the specified string to the screen.
         * Uses the specified color.
         *\param text The text to write.
         *\param color The color to write the text in.
         *\sa fillcolor(color)*/
        void write(const std::string& text, Color color);
        
        /**\brief Puts the current shape of this turtle on the screen
         *        with the current fill color and the outline of the shape.
         *\return The stamp ID of the put stamp.*/
        int stamp();
        /**\brief Removes the stamp with the specified ID.*/
        void clearstamp(int stampid);
        /**\brief Removes all stamps with an ID less than that which is specified.
         *        If the specified stampid is less than 0, it removes ALL stamps.*/
        void clearstamps(int stampid = -1);

        /**\brief Sets the shape of this turtle.
         *\param p The polygon to derive shape geometry from.*/
        void shape(const AbstractDrawableObject& p) {
            pushState();
            state->cursor.reset(p.copy());
            updateParent(false, false);
        }

        /**\brief Sets the shape of this turtle from the specified shape name.
         *\param name The name of the shape to set.*/
        void shape(const std::string& name);

        /**\brief Returns the shape of this turtle.*/
        const AbstractDrawableObject& shape() {
            return *state->cursor;
        }

        /**\brief Undoes the previous action of this turtle.*/
        bool undo(bool try_redraw = true);

        /**\brief Set, or disable, the undo buffer.
         *\param size The size of the undo buffer.*/
        void setundobuffer(unsigned int size) {
            if (size < 1)//clamp lower bound to 1
                size = 1;

            undoStackSize = size;
            while (stateStack.size() > size) {
                stateStack.pop_front();
            }
        }

        /**\brief Returns the size of the undo stack.*/
        unsigned int undobufferentries() {
            return static_cast<unsigned int>(stateStack.size());
        }

        /**\brief Sets the speed of this turtle in range of 0 to 10.
         *\param The speed of the turtle, in range of 0 to 10.
         *\sa cturtle::TurtleSpeed*/
        void speed(float val) {
            pushState();
            state->moveSpeed = val;
        }

        /**\brief Returns the speed of this turtle.*/
        float speed() {
            return state->moveSpeed;
        }

        /**\brief Applies a rotation to the */
        void tilt(float angle);

        /**\brief Returns the rotation of the cursor. Not the heading,
         *        or the angle at which the forward function will move.*/
        float tilt() const {
            return state->angleMode ? state->cursorTilt : toDegrees(state->cursorTilt);
        }

        /**\brief Set whether or not the turtle is being shown.
         *\param state True when showing, false othewise.*/
        void setshowturtle(bool state);

        /**\brief Shows the turtle.
         *        Equivalent to calling setshowturtle(true).
         *\sa setshowturtle(bool)*/
        inline void showturtle() {
            setshowturtle(true);
        }

        /**\brief Hides the turtle.
         *\sa setshowturtle(bool)*/
        inline void hideturtle() {
            setshowturtle(false);
        }

        /**\brief Sets whether or not the pen is down.*/
        void setpenstate(bool down);

        /**\brief Brings the pen up.*/
        inline void penup() {
            setpenstate(false);
        }

        /**\brief Brings the pen down.*/
        inline void pendown() {
            setpenstate(true);
        }

        /**\brief Sets the pen color.
         *\param c The color used by the pen; the color of lines between movements.*/
        void pencolor(Color c) {
            pushState();
            state->penColor = c;
            updateParent(false, false);
        }

        /**\brief Returns the pen color; the color of the lines between movements.
         *\return The color of the pen.*/
        Color pencolor() const {
            return state->penColor;
        }

        /**Sets the width of the pen line.
         *\param pixels The total width, in pixels, of the pen line.*/
        void width(int pixels) {
            pushState();
            state->penWidth = pixels;
        }

        /**Returns the width of the pen line.
         *\return The width of the line, in pixels.*/
        int width() const{
            return state->penWidth;
        }

        /**\brief Draws this turtle on the specified canvas with the specified transform.
         *\param screenTransform The transform at which to draw the turtle objects.
         *\param canvas The canvas on which to draw this turtle.*/
        void draw(const Transform& screenTransform, Image& canvas);

        /**Sets this turtle to use angles measured in degrees.
         *\sa radians()*/
        void degrees() {
            pushState();
            state->angleMode = false;
        }

        /**Sets this turtle to use angles measured in radians.
         *\sa degress()*/
        inline void radians() {
            pushState();
            state->angleMode = true;
        }

        /**\brief Resets this turtle.
         * Moves this turtle home, resets all pen attributes,
         * and removes all previously added scene objects.*/
        void reset();

        /**Sets this turtles screen.*/
        void setScreen(AbstractTurtleScreen* scr) {
            screen = scr;
        }

        /**\brief Empty virtual destructor.*/
        virtual ~Turtle() {}
    protected:
        std::list<std::list<SceneObject>::iterator> objects;
        std::list<PenState> stateStack = {PenState()};
        std::list<Line> fillLines;

        //lines to be drawn to temp screen when filling to avoid invalidating screen
        Transform* transform = nullptr;
        PenState* state = nullptr;

        /**These variables are used to draw the "travel" line when
         * the turtle is traveling. (e.g, the line between where it's going*/
        Point travelPoints[2];
        bool traveling = false;

        /*Undo stack size.*/
        unsigned int undoStackSize = 100;

        /*Accumulator for fill state*/
        Polygon fillAccum;

        /*Screen pointer. Assign before calling any other function!*/
        AbstractTurtleScreen* screen = nullptr;

        /**Pushes a copy of the pen's state on the stack.*/
        void pushState();
        /**Pops the top of the pen's state stack.*/
        bool popState();

        /**
         * \brief Internal function used to add geometry to the turtle screen.
         * \param t The transform of the geometry.
         * \param color The color of the geometry.
         * \param geom The geometry to add.
         * \return A boolean indicating if the geometry was added to the scene.
         */
        bool pushGeom(const Transform& t, AbstractDrawableObject* geom);

        /**\brief Internal function used to add a stamp object to the turtle screen.
         *\param t The transform at which to draw the stamp.
         *\param color The color with which to draw the stamp.
         *\param geom The geometry of the stamp.*/
        bool pushStamp(const Transform& t, AbstractDrawableObject* geom);

        /**\brief Internal function used to add a text object to the turtle screen.
         *\param t The transform at which to draw the text.
         *\param color The color with which to draw the text.
         *\param text The string to draw.*/
        bool pushText(const Transform& t, Color color, const std::string& text);

        /**\brief Internal function used to add a trace line object to the turtle screen.
         *\param a Point A
         *\param b Point B*/
        bool pushTraceLine(Point a, Point b);

        /**Returns the speed, of any applicable animation
          in milliseconds, based off of this turtle's speed setting.*/
        long int getAnimMS() {
            //300 is the "scale" animations adhere to.
            //The longest animation is 300 milliseconds, shortest is 0.
            //This was an arbitrary choice, trying to match the speed of the Python implementation.
            return screen->supports_live_animation() ? state->moveSpeed <= 0 ? 0 : long(((11.0f - state->moveSpeed) / 10.0f) * 300) : 0;
        }

        /**Conditionally calls the parent screen's update function.*/
        void updateParent(bool invalidate = false, bool input = true);

        /**Performs an interpolation, with animation,
         * between the source transform and the destination transform.
         * May push a new fill vertex if filling and pushing state, and applies appropriate
         * lines if the pen is down. Generally manages all state related
         * to movement as a side effect.*/
        void travelBetween(Transform from, const Transform& to, bool pushState);

        /**Performs an interpolation, with animation,
         * between the current transform and the specified one.
         * Pushes a new fill vertex if filling, and applies appropriate
         * lines if the pen is down. Does push the state stack.*/
        void travelTo(const Transform& dest){
            travelBetween(*transform, dest, true);
        }

        /**Performs an interpolation, with animation,
         * between the current transformation and the previous one.
         * Will *not* push the state stack.
         * ENSURE STACK IS BIG ENOUGH TO DO THIS BEFORE CALLING.*/
        void travelBack(){
            travelBetween(*transform, std::prev(stateStack.end(), 2)->transform, false);
        }

        /**Inheritors must assign screen pointer!*/
        Turtle() {}
    };

#ifdef CTURTLE_HEADLESS
    /*Used to output Base-64 GIF and HTML source for OfflineTurtleScreen.*/
    inline std::string encodeFileBase64(const std::string& path){
        std::ifstream file(path, std::ios::binary | std::ios::ate);
        std::streamsize size = file.tellg();
        file.seekg(0, std::ios::beg);

        std::vector<unsigned char> buffer(size, 0);
        file.read((char*)buffer.data(), size);
        return base64::encode(buffer);
    }

    class OfflineTurtleScreen : public AbstractTurtleScreen{
    public:
        OfflineTurtleScreen(){
            const int width = CTURTLE_HEADLESS_WIDTH;
            const int height = CTURTLE_HEADLESS_HEIGHT;
            canvas.assign(width, height, 1, 3);
            canvas.fill(255);
            isClosed = false;
            gif = jo_gif_start(CTURTLE_HEADLESS_SAVEDIR, width, height,1, 31);
            redraw(true);
        }

        ~OfflineTurtleScreen(){
            bye();
        }

        void tracer(int countmax, unsigned int delayMS = 10){
            redrawCounterMax = countmax;
            delay(delayMS);
            redraw();
        }

        int window_width() const{
            return canvas.width();
        }

        int window_height() const{
            return canvas.height();
        }

        Color bgcolor() const{
            return backgroundColor;
        }

        void bgcolor(const Color& c){
            backgroundColor = c;
            redraw(true);
        }

        void mode(ScreenMode mode){
            //Resets & re-orients all turtles.

            curMode = mode;
            for (Turtle* t : turtles) {
                t->reset();
            }
        }

        ScreenMode mode() const{
            return curMode;
        }

        void clearscreen(){
            //1) Delete all drawings and turtles
            //2) White background

            for (Turtle* turtle : turtles) {
                turtle->setScreen(nullptr);
            }

            turtles.clear();
            backgroundColor = Color("white");
            curMode = SM_STANDARD;
        }

        void resetscreen(){
            for (Turtle* turtle : turtles)
                turtle->reset();
        }

        ivec2 screensize(Color& bg){
            bg = backgroundColor;
            return {canvas.width(), canvas.height()};
        };
        //code-smell from python->c++, considering separation of functionality

        ivec2 screensize(){
            return {canvas.width(), canvas.height()};
        }

        void update(bool invalidateDraw = false, bool processInput = false){
            redraw(invalidateDraw);
            //processInput is ignored. OfflineTurtleScreen does NOT support input.
        }

        void delay(unsigned int ms){
            delayMS = ms;
        }

        unsigned int delay(){
            return delayMS;
        }

        void bye() {
            if(isClosed)
                return;

            /*finish up drawing if redraw counter hasn't been met*/
            if(redrawCounter > 0 || redrawCounter >= redrawCounterMax){
                tracer(1, delayMS);
            }
            
            jo_gif_end(&gif);

#ifndef CTURTLE_HEADLESS_NO_HTML
            /*print base-64 encoding + HTML source*/
            std::string imgCode = encodeFileBase64(CTURTLE_HEADLESS_SAVEDIR);

            //See the following to understand why this was done:
            //https://github.com/ericsonga/APCSAReview/blob/master/_sources/TurtleGraphics/turtleBasics.rst
            //HTML can be captured for later output.
            std::cout << "<img src=\'data:image/gif;base64,";
            std::cout << imgCode;
            std::cout << "\'/>";
#endif

            clearscreen();
            isClosed = true;
        }

        Image& getcanvas(){
            return canvas;
        }

        bool isclosed(){
            return isClosed;
        }

        bool supports_live_animation() const{
            return false;
        }

        virtual void redraw(bool invalidate = false){
            if (isclosed())
                return;
            int fromBack = 0;
            bool hasInvalidated = invalidate;

            //Handle resizes.

            if (lastTotalObjects <= objects.size()) {
                fromBack = static_cast<int>(objects.size() - lastTotalObjects);
            }

            if (hasInvalidated) {
                canvas.draw_rectangle(0, 0, canvas.width(), canvas.height(), backgroundColor.rgbPtr());
                redrawCounter = 0;//Forced redraw due to canvas invalidation.
            } else {
                if(redrawCounterMax == 0){
                    return;
                }

                redrawCounter++;

                if (redrawCounter >= redrawCounterMax) {
                    redrawCounter = 0;
                } else {
                    return;
                }
            }

            auto latestIter = !hasInvalidated ? std::prev(objects.end(), fromBack) : objects.begin();

            Transform screen = screentransform();
            while (latestIter != objects.end()) {
                SceneObject& object = *latestIter;
                const Transform t(screen.copyConcatenate(object.transform));

                object.geom->draw(t, canvas);

                latestIter++;
            }

            if (canvas.width() != turtleComposite.width() || canvas.height() != turtleComposite.height()) {
                turtleComposite.assign(canvas);
            } else {
                //This works off the assumption that drawImage is accelerated.
                //There might be a more efficient way to do this, however.
                turtleComposite.draw_image(0, 0, canvas);
            }

            for (Turtle* turt : turtles)
                turt->draw(screen, turtleComposite);

            lastTotalObjects = static_cast<int>(objects.size());

            /* The following code takes the place of swapping the display buffer for the canvas,
             * which is what the interactive mode does.*/

            //This copy is NOT efficient.
            //We should be able to take advantage of loop unrolling here
            for(int x = 0; x < CTURTLE_HEADLESS_WIDTH; x++){
                for(int y = 0; y < CTURTLE_HEADLESS_HEIGHT; y++){
                    uint8_t* pixel = (&gifWriteBuffer[(y*CTURTLE_HEADLESS_WIDTH+x)*4]);

                    pixel[0] = turtleComposite(x,y,0);
                    pixel[1] = turtleComposite(x,y,1);
                    pixel[2] = turtleComposite(x,y,2);
                    pixel[3] = 255;
                }
            }

            //GIF frames are measured in centiseconds, thus the /10 on the delayMS...
            jo_gif_frame(&gif, gifWriteBuffer, delayMS / 10, true);
        }

        Transform screentransform() const{
            return Transform().translate(canvas.width()/2, canvas.height()/2).scale(1, -1.0f);
        }

        void add(Turtle& turtle){
            turtles.push_back(&turtle);
        }

        std::list<SceneObject>& getScene(){
            return objects;
        }

        AbstractDrawableObject& shape(const std::string& name){
            return shapes[name];
        }
    private:
        /*this can be a constant allocated buffer.*/
        uint8_t gifWriteBuffer[CTURTLE_HEADLESS_WIDTH * CTURTLE_HEADLESS_HEIGHT*4];
        //allocate enough to hold width*height*4 (4 because RGBA).
        //this fits into uint32_t type quite nicely. (8+8+8+8 bits, r+g+b+a) = 32

        //This struct controls the writing of resulting GIFs.
        jo_gif_t gif;

        std::list<SceneObject> objects;
        std::list<Turtle*>      turtles;

        bool isClosed = true;
        Image canvas;

        //The turtle composite image.
        //This image copies the canvas and has
        //turtles drawn to it to avoid redrawing a "busy" canvas.
        //Trace lines are also drawn on this when filling.
        Image turtleComposite;

        /**The total objects on screen the last time this screen was drawn.
         * Used to keep track of newer scene objects for a speed improvement.*/
        int lastTotalObjects = 0;

        /**The background color of this TurtleScreen.*/
        Color backgroundColor = Color("white");

        //OfflineTurtleScreen has no background image.

        /**The current screen mode.
         *\sa mode(m)*/
        ScreenMode curMode = SM_STANDARD;

        /**Redraw delay, in milliseconds.*/
        long int delayMS = 10;

        /** These variables are used specifically in tracer settings.**/
        /**Redraw Counter.*/
        int redrawCounter = 0;
        /**Redraw counter max.*/
        int redrawCounterMax = 1;

        //Default shapes.
        std::unordered_map<std::string, Polygon> shapes = {
                //counterclockwise coordinates.
                {"triangle",
                        Polygon{
                                {0, 0},
                                {-5, 5},
                                {5, 5}}},
                {"square",
                        Polygon{
                                {-5, -5},
                                {-5, 5},
                                {5, 5},
                                {5, -5}}},
                {"indented triangle",
                        Polygon{
                                //CCW
                                {0, 0},
                                {-5, 10},
                                {0, 8},
                                {5, 10}}},
                {"arrow",
                        Polygon{
                                {0, 0},
                                {-5, 5},
                                {-3, 5},
                                {-3, 10},
                                {3, 10},
                                {3, 5},
                                {5, 5}}}
        };
    };

    typedef OfflineTurtleScreen TurtleScreen;
#else /*NOT DEFINED CTURTLE_HEADLESS*/
    constexpr int SCREEN_DEFAULT_WIDTH = 800;
    constexpr int SCREEN_DEFAULT_HEIGHT = 600;
    /**
     * InteractiveTurtleScreen
     * Holds and maintains facilities in relation to displaying
     * turtles and consuming input events from users through callbacks.
     * This includes holding the actual data for a given scene after being
     * populated by Turtle. It layers draw calls in the order they are called,
     * independent of whatever Turtle object creates it.
     *
     * \sa Turtle
     */
    class InteractiveTurtleScreen : public AbstractTurtleScreen{
    public:

        /**Empty constructor.
         * Assigns an 800 x 600 pixel display with a title of "CTurtle".*/
        InteractiveTurtleScreen() : display(SCREEN_DEFAULT_WIDTH, SCREEN_DEFAULT_HEIGHT, "CTurtle", 0) {
            canvas.assign(display);
            initEventThread();
            redraw(true);
        }

        /**Title constructor.
         * Assigns an 800 x 600 pixel display with a specified title.
         *\param title The title to assign the display with.*/
        InteractiveTurtleScreen(const std::string& title) : display(SCREEN_DEFAULT_WIDTH, SCREEN_DEFAULT_HEIGHT, title.c_str(), 0) {
            display.set_normalization(0);
            canvas.assign(display);
            initEventThread();
            redraw(true);
        }

        /**Width, height, and title constructor.
         * Assigns the display with the specified dimensions, in pixels, and
         * assigns the display the specified title.
         *\param width The width of the display, in pixels.
         *\param height The height of the display, in pixels.
         *\param title The title of the display.*/
        InteractiveTurtleScreen(int width, int height, const std::string& title = "CTurtle")
            : display(width, height) {
            display.set_title(title.c_str());
            display.set_normalization(0);
            canvas.assign(display);
            initEventThread();
            redraw(true);
        }

        /**Destructor. Calls "bye" function.*/
        ~InteractiveTurtleScreen() {
            bye();
        }

        /**Sets an internal variable that dictates how many frames
         * are skipped between screen updates; higher numbers will
         * speed up complex turtle drawings. Setting it to ZERO will
         * COMPLETELY disable animation until this value changes.
         *\param countmax The value of the aforementioned variable.
         *\param delayMS This value is sent to function "delay".*/
        void tracer(int countmax, unsigned int delayMS = 10) {
            redrawCounterMax = countmax;
            delay(delayMS);
            redraw();
        }

        /**Sets the background color of the screen.
         * Please note that, if there is a background image, this color is not
         * applied until it is removed.
         *\param color The background color.
         *\sa bgpic(image)*/
        void bgcolor(const Color& color){
            backgroundColor = color;
            redraw(true);
        }

        /**Returns the background color of the screen.
         *\return The background color of the screen.*/
        Color bgcolor() const{
            return backgroundColor;
        }

        /**\brief Sets the background image of the display.
         * Sets the background image. Please note that the background image
         * takes precedence over background color.
         *\param img The background image.*/
        void bgpic(const Image& img){
            backgroundImage.assign(img);
            backgroundImage.resize(window_width(), window_height());
            redraw(true);
        }

        /**Returns a const reference to the background image.*/
        const Image& bgpic(){
            return backgroundImage;
        }

        bool supports_live_animation() const{
            return true;
        }

        /**Sets the screen mode of this screen.
         *\param mode The screen mode.
         *\todo Refine this documentation.*/
        void mode(ScreenMode mode){
            curMode = mode;
            for (Turtle* t : turtles) {
                t->reset();
            }
        }

        /**Returns the screen mode of this screen.*/
        ScreenMode mode() const {
            return curMode;
        }

        /**\brief Clears this screen.
         * Deletes all drawings and turtles,
         * Resets the background to plain white,
         * Clears all event bindings,
         */
        void clearscreen(){
            //1) Delete all drawings and turtles
            //2) White background
            //3) No background image
            //4) No event bindings

            for (Turtle* turtle : turtles) {
                turtle->setScreen(nullptr);
            }

            turtles.clear();
            backgroundColor = Color("white");
            backgroundImage.assign();//assign with no parameters is deleting whatever contents it may have.
            curMode = SM_STANDARD;

            //Gotta do binding alterations under the cache's mutex lock.
            eventCacheMutex.lock();
            timerBindings.clear();
            keyBindings[0].clear();
            keyBindings[1].clear();
            for (int i = 0; i < 3; i++)
                mouseBindings[i].clear();
            eventCacheMutex.unlock();
        }

        /**Alias for clearscreen function
         *\sa clearscreen()*/
        inline void clear() {
            clearscreen();
        }

        /**Resets all turtles belonging to this screen to their original state->*/
        void resetscreen(){
            for (Turtle* turtle : turtles)
                turtle->reset();
        }

        /**Resets all turtles belonging to this screen to their original state->*/
        inline void reset() {
            resetscreen();
        }

        /**Returns the size of this screen, in pixels.
          Also returns the background color of the screen,
          by assigning the input reference.*/ //code-smell from python->c++, considering separation of functionality
        inline ivec2 screensize(Color& bg){
            bg = backgroundColor;
            return {display.screen_width(), display.screen_height()};
        }

        /**Returns the size of the screen, in pixels.*/
        inline ivec2 screensize() { //see line above comment about code-smell
            return {display.screen_width(), display.screen_height()};
        }

        /**Updates the screen's graphics and input.
         *\param invalidateDraw Completely redraws the scene if true.
         *                      If false, only draws the newest geometry.
         *\param processInput A boolean indicating to process input.*/
        void update(bool invalidateDraw = false, bool processInput = true){
            /*Resize canvas when necessary.*/
            if (display.is_resized()) {
                display.resize();
                invalidateDraw = true;
            }
            redraw(invalidateDraw);

            if (processInput && !timerBindings.empty()) {
                //Call timer bindings first.
                uint64_t curTime = detail::epochTime();
                for (auto& timer : timerBindings) {
                    auto& func = std::get<0>(timer);
                    uint64_t reqTime = std::get<1>(timer);
                    uint64_t& lastCalled = std::get<2>(timer);

                    if (curTime >= lastCalled + reqTime) {
                        lastCalled = curTime;
                        func();
                    }
                }
            }

            /**No events to process in the cache, or we're not processing it right now.*/
            if (cachedEvents.empty() || !processInput)
                return; //No events to process.

            //lock event cache to avoid race conditions
            eventCacheMutex.lock();

            for (InputEvent& event : cachedEvents) {
                if (event.type) {//process keyboard event
                    KeyFunc& keyFunc = *reinterpret_cast<KeyFunc*> (event.cbPointer);
                    keyFunc();
                } else {//process mouse event
                    MouseFunc& mFunc = *reinterpret_cast<MouseFunc*> (event.cbPointer);
                    mFunc(event.mX, event.mY);
                }
            }

            cachedEvents.clear();
            eventCacheMutex.unlock();
        }

        /**Sets the delay set between turtle commands.*/
        void delay(unsigned int ms){
            delayMS = ms;
        }

        /**Returns the delay set between screen swaps in milliseconds.*/
        unsigned int delay(){
            return delayMS;
        }

        /**Returns the width of the window, in pixels.*/
        int window_width() const {
            return display.window_width();
        }

        /**Returns the height of the window, in pixels.*/
        int window_height() const {
            return display.window_height();
        }

        /**Saves the display as a file, the format of which is dependent
          on the file extension given in the specified file path string.*/
        void save(const std::string& file) {
            Image screenshotImg;
            display.snapshot(screenshotImg);
            screenshotImg.save(file.c_str());
        }

        /**Enters a loop, lasting until the display has been closed,
         * which updates the screen. This is useful for programs which
         * rely heavily on user input, as events are still called like normal.*/
        void mainloop() {
            while (!display.is_closed()) {
                update(false, true);
                std::this_thread::yield();//Yield repetitive loops on mainloop to avoid high-cpu usage.
            }
        }

        /**Resets and closes this display.*/
        void bye(){
            if(redrawCounter > 0 || redrawCounter >= redrawCounterMax){
                tracer(1, delayMS);
            }

            if (eventThread.get() != nullptr) {
                killEventThread = true;
                eventThread->join();
                eventThread.reset(nullptr);
            }

            clearscreen();

            if (!display.is_closed())
                display.close();
        }

        /**Returns the canvas image used by this screen.*/
        Image& getcanvas() {
            return canvas;
        }

        /**Returns the internal CImg display.*/
        cimg::CImgDisplay& internaldisplay() {
            return display;
        }

        /**Returns a boolean indicating if the
          screen has been closed.*/
        inline bool isclosed() {
            return internaldisplay().is_closed();
        }

        /**Draws all geometry from all child turtles and swaps this display.*/
        void redraw(bool invalidate = false){
            if (isclosed())
                return;
            int fromBack = 0;
            bool hasInvalidated = invalidate;

            //Handle resizes.
            if (display.window_width() != canvas.width() || display.window_height() != canvas.height()) {
                canvas.resize(display);
                hasInvalidated = true;
            }

            if (lastTotalObjects <= objects.size()) {
                fromBack = static_cast<int>(objects.size() - lastTotalObjects);
            }

            if (hasInvalidated) {
                if(!backgroundImage.is_empty()) {
                    canvas.assign(backgroundImage);
                } else {
                    canvas.draw_rectangle(0, 0, canvas.width(), canvas.height(), backgroundColor.rgbPtr());
                }
                redrawCounter = 0;//Forced redraw due to canvas invalidation.
            } else {
                if(redrawCounterMax == 0){
                    return;
                }

                redrawCounter++;

                if (redrawCounter >= redrawCounterMax) {
                    redrawCounter = 0;
                } else {
                    return;
                }
            }

            auto latestIter = !hasInvalidated ? std::prev(objects.end(), fromBack) : objects.begin();

            Transform screen = screentransform();
            while (latestIter != objects.end()) {
                SceneObject& object = *latestIter;
                const Transform t(screen.copyConcatenate(object.transform));

                object.geom->draw(t, canvas);

                latestIter++;
            }

            if (canvas.width() != turtleComposite.width() || canvas.height() != turtleComposite.height()) {
                turtleComposite.assign(canvas);
            } else {
                //This works off the assumption that drawImage is accelerated.
                //There might be a more efficient way to do this, however.
                turtleComposite.draw_image(0, 0, canvas);
            }

            for (Turtle* turt : turtles)
                turt->draw(screen, turtleComposite);

            lastTotalObjects = static_cast<int>(objects.size());
            display.display(turtleComposite);
            detail::sleep(delayMS);
        }

        /**Returns the screen-level Transform
          of this screen. This is what puts the origin
          at the center of the screen rather than at
          at the top left, for example.*/
        Transform screentransform() const {
            //Scale negatively on Y axis to match
            //Python's coordinate system.
            //without this scaling, top left is 0,0
            //instead of the bottom left (which is 0,Y without the scaling)
            return Transform().translate(canvas.width()/2, canvas.height()/2).scale(1, -1.0f);
        }

        /**\brief Adds an additional "on press" key binding for the specified key.
         *\param func The function to call when the specified key is pressed.
         *\param key The specified key.*/
        void onkeypress(KeyFunc func, KeyboardKey key) {
            eventCacheMutex.lock();
            //determine if key list exists
            if (keyBindings[0].find(key) == keyBindings[0].end()) {
                keyBindings[0][key] = std::list<KeyFunc>();
            }
            //then push it to the end of the list
            keyBindings[0][key].push_back(func);
            eventCacheMutex.unlock();
        }

        /**\brief Adds an additional "on press" key binding for the specified key.
         *\param func The function to call when the specified key is released.
         *\param key The specified key.*/
        virtual void onkeyrelease(KeyFunc func, KeyboardKey key) {
            eventCacheMutex.lock();
            //determine if key list exists, if not, make one
            if (keyBindings[1].find(key) == keyBindings[1].end()) {
                keyBindings[1][key] = std::list<KeyFunc>();
            }
            //then push it to the end of the list
            keyBindings[1][key].push_back(func);
            eventCacheMutex.unlock();
        }

        /**\brief Simulates a key "on press" event.
         *\param key The key to call "on press" bindings for.*/
        void presskey(KeyboardKey key) {
            if (keyBindings[0].find(key) == keyBindings[0].end())
                return;
            for (const KeyFunc& func : keyBindings[0][key]) {
                func();
            }
        }

        /**\brief Simulates a key "on release" event.
         *\param key The key to call "on release" bindings for.*/
        void releasekey(KeyboardKey key) {
            if (keyBindings[1].find(key) == keyBindings[1].end())
                return;
            for (KeyFunc& func : keyBindings[1][key]) {
                func();
            }
        }

        /**\brief Adds an additional "on click" mouse binding for the specified button.
         *\param func The function to call when the specified button is clicked.
         *\param button The specified button.*/
        void onclick(MouseFunc func, MouseButton button = MOUSEB_LEFT) {
            eventCacheMutex.lock();
            mouseBindings[button].push_back(func);
            eventCacheMutex.unlock();
        }

        /**Calls all previously added mouse button call-backs.
         *\param x The X coordinate at which to press.
         *\param y The Y coordinate at which to press.
         *\param button The button to simulate being pressed.*/
        void click(int x, int y, MouseButton button) {
            eventCacheMutex.lock();
            for (MouseFunc& func : mouseBindings[button]) {
                func(x, y);
            }
            eventCacheMutex.unlock();
        }

        /**\copydoc click(int, int, MouseButton)*/
        inline void click(const Point& pt, MouseButton button){
            click(pt.x, pt.y, button);
        }

        /**\brief Adds a timer function to be called every N milliseconds.
         *\param func The function to call when the timer has finished.
         *\param time The total number of milliseconds between calls.*/
        void ontimer(TimerFunc func, unsigned int time) {
            timerBindings.push_back(std::make_tuple(func, time, detail::epochTime()));
        }

        /**Binds the "bye" function to the onclick event for the left
         * mouse button.*/
        void exitonclick() {
            //Catch up visually before entering event loop, when necessary.
            if(redrawCounter > 0 || redrawCounter >= redrawCounterMax){
                tracer(1, delayMS);
            }
            
            onclick([&](int x, int y) {
                display.close();
            });
            mainloop();
        }

        /**Adds the specified turtle to this screen.*/
        void add(Turtle& turtle) {
            turtles.push_back(&turtle);
        }

        /**Returns a reference to the list of scene objects.
         * This list is used to redraw the screen.*/
        std::list<SceneObject>& getScene() {
            return objects;
        }

        /**
         * Returns the shape associated with the specified name.
         * @param name
         * @return
         */
        AbstractDrawableObject& shape(const std::string& name) {
            return shapes[name];
        }
    protected:
        /**The underlying display mechanism for a TurtleScreen.*/
        cimg::CImgDisplay display;

        /**The canvas onto which scene objects are drawn to.*/
        Image canvas;

        //The turtle composite image.
        //This image copies the canvas and has
        //turtles drawn to it to avoid redrawing a "busy" canvas.
        //Trace lines are also drawn on this when filling.
        Image turtleComposite;

        /**The total objects on screen the last time this screen was drawn.
         * Used to keep track of newer scene objects for a speed improvement.*/
        int lastTotalObjects = 0;

        /**The background color of this TurtleScreen.*/
        Color backgroundColor = Color("white");
        /**The background image of this TurtleScreen.
         * When not empty, this image takes precedence over
         * the background color when drawing.**/
        Image backgroundImage;
        /**The current screen mode.
         *\sa mode(m)*/
        ScreenMode curMode = SM_STANDARD;

        /**Redraw delay, in milliseconds.*/
        long int delayMS = 10;

        /** These variables are used specifically in tracer settings.**/
        /**Redraw Counter.*/
        int redrawCounter = 0;
        /**Redraw counter max.*/
        int redrawCounterMax = 1;

        /**Initializes the underlying event thread.
         * This thread is cleanly managed and destroyed
         * when its owning object is destroyed.
         * The thread just populates the cachedEvents list,
         * so that events may be processed in the main thread.*/
        void initEventThread(){
            eventThread.reset(new std::thread([&]() {
                //Mouse button states, between updates.
                //Keeps track of release/press etc
                //states for all three mouse buttons for isDown.
                //*importantly, this allows us to avoid repeated events.
                bool mButtons[3] = {false, false, false};
                //Same thing for keys here.
                //(this is a list of keys marked as being in a "down" state)
                std::list<KeyboardKey> mKeys;

                while (!display.is_closed() && !killEventThread) {
                    //Updates all input.
                    if (!display.is_event()) {
                        std::this_thread::yield();
                        continue;
                    }

                    eventCacheMutex.lock();

                    Transform mouseOffset = screentransform();
                    Point mousePos = {
                            static_cast<int>((static_cast<float>(display.mouse_x()) - mouseOffset.getTranslateX()) * mouseOffset.getScaleX()),
                            static_cast<int>((static_cast<float>(display.mouse_y()) - mouseOffset.getTranslateY()) * mouseOffset.getScaleY())
                    };

                    //Update mouse button input.
                    const unsigned int button = display.button();
                    bool buttons[3] = {
                            button & 1, //left
                            button & 2, //right
                            button & 4 //middle
                    };

                    for (int i = 0; i < 3; i++) {
                        if (!(!mButtons[i] && buttons[i]))//is this button state "down"?
                            continue; //if not, skip its processing loop.

                        for (MouseFunc& func : mouseBindings[i]) {
                            //append to the event cache.
                            InputEvent e;
                            e.type = false;
                            e.mX = mousePos.x;
                            e.mY = mousePos.y;
                            e.cbPointer = reinterpret_cast<void*> (&func);
                            cachedEvents.push_back(e);
                        }
                    }

                    const auto& keys = NAMED_KEYS;

                    //iterate through every key to determine its state,
                    //then call the appropriate callbacks.
                    for (const auto& keyPair : keys) {
                        KeyboardKey key = keyPair.second;
                        const bool lastDown = std::find(mKeys.begin(), mKeys.end(), key) != mKeys.end();
                        const bool curDown = display.is_key((unsigned int) key);

                        int state = -1;
                        if (!lastDown && curDown) {
                            //Key down.
                            state = 0;
                            mKeys.push_back(key);
                        } else if (lastDown && !curDown) {
                            //Key up.
                            state = 1;
                            mKeys.remove(key);
                        } else continue; //skip on case where it was down and is down

                        try {
                            //will throw if no bindings available for key,
                            //and that's perfectly fine, so we just silently catch
                            auto& bindingList = keyBindings[state][key];
                            for (auto& cb : bindingList) {
                                cb();
                            }
                        } catch (...) {}
                    }

                    mButtons[0] = buttons[0];
                    mButtons[1] = buttons[1];
                    mButtons[2] = buttons[2];
                    eventCacheMutex.unlock();
                }
            }));
        }

        /**The scene list.*/
        std::list<SceneObject> objects;

        /**The list of attached turtles.*/
        std::list<Turtle*> turtles;

        /**A unique pointer to the event thread.
         *\sa initEventThread()*/
        std::unique_ptr<std::thread> eventThread;
        /**A list of cached events. Filled by event thread,
         * processed and emptied by main thread.*/
        std::list<InputEvent> cachedEvents;
        /**A boolean indicating whether or not to kill the event thread.*/
        bool killEventThread = false;
        /**The mutex which controls synchronization between the main
         * thread and the event thread.*/
        std::mutex eventCacheMutex;

        //this is an array. 0 for keyDown bindings, 1 for keyUp bindings.
        std::unordered_map<KeyboardKey, std::list<KeyFunc>> keyBindings[2] = {
            {},
            {}
        };
        //similar, mouseb_left mouseb_middle mouseb_right bindings.
        std::list<MouseFunc> mouseBindings[3] = {
            {},
            {},
            {}
        };
        //timer bindings, one function per originating time and delta.
        std::list<std::tuple<TimerFunc, uint64_t, uint64_t>> timerBindings;

        //Default shapes.
        std::unordered_map<std::string, Polygon> shapes = {
            //counterclockwise coordinates.
            {"triangle",
                Polygon{
                    {0, 0},
                    {-5, 5},
                    {5, 5}}},
            {"square",
                Polygon{
                    {-5, -5},
                    {-5, 5},
                    {5, 5},
                    {5, -5}}},
            {"indented triangle",
                Polygon{
                    //CCW
                    {0, 0},
                    {-5, 10},
                    {0, 8},
                    {5, 10}}},
            {"arrow",
                Polygon{
                    {0, 0},
                    {-5, 5},
                    {-3, 5},
                    {-3, 10},
                    {3, 10},
                    {3, 5},
                    {5, 5}}}
        };
    };

    typedef InteractiveTurtleScreen TurtleScreen;
#endif /*CTURTLE_HEADLESS*/

    //SECTION: TURTLE IMPLEMENTATION

    Turtle::Turtle(AbstractTurtleScreen& scr) {
        screen = &scr;
        screen->add(*this);
        reset();
    }

    //write

    void Turtle::write(const std::string& text) {
        pushText(*transform, state->fillColor, text);
        updateParent(false, false);
    }
    
    void Turtle::write(const std::string &text, Color color) {
        pushText(*transform, color, text);
        updateParent(false, false);
    }

    //Stamps

    int Turtle::stamp() {
        pushStamp(*transform, state->cursor.get()->copy());
        return state->curStamp;
    }

    void Turtle::clearstamp(int stampid) {
        auto iter = objects.begin(); //iterator which holds an iterator to the screen's scene list.

        while (iter != objects.end()) {
            auto& objIter = *iter;
            if (objIter->stamp && objIter->stampid == stampid) {
                break;
            }
            iter++;
        }

        if (iter != objects.end()) {
            objects.erase(iter);

            if (screen != nullptr) {
                screen->getScene().erase(*iter);
            }
        }

        updateParent(true,false);
    }

    void Turtle::clearstamps(int stampid) {
        typedef decltype(objects.begin()) iter_t;

        std::list<iter_t> removals;

        iter_t iter = objects.begin();
        while (iter != objects.end()) {
            auto& objIter = *iter;
            if (stampid < 0 ? objIter->stamp : (objIter->stamp && objIter->stampid <= stampid)) {
                removals.push_back(iter);
            }
            iter++;
        }

        for (iter_t& iter : removals) {
            screen->getScene().erase(*iter);
            objects.erase(iter);
        }
        updateParent(true, false);
    }

    void Turtle::shape(const std::string& name) {
        pushState();
        state->cursor.reset((screen->shape(name).copy()));
        updateParent(false, false);
    }

    //Movement

    void Turtle::forward(int pixels) {
        if (screen == nullptr)
            return;
        travelTo(Transform(*transform).forward(static_cast<float>(pixels)));
    }

    void Turtle::backward(int pixels) {
        if (screen == nullptr)
            return;
        travelTo(Transform(*transform).backward(static_cast<float>(pixels)));
    }

    void Turtle::right(float amt) {
        amt = state->angleMode ? -amt : -toRadians(amt);
        //Flip angle orientation based on screen mode.
        travelTo(Transform(*transform).rotate(amt));
    }

    void Turtle::left(float amt) {
        amt = state->angleMode ? amt : toRadians(amt);
        
        //Flip angle orientation based on screen mode.
        travelTo(Transform(*transform).rotate(amt));
    }

    void Turtle::setheading(float amt) {
        //Swap to correct unit if necessary.
        amt = state->angleMode ? amt : toRadians(amt);
        //Flip angle orientation based on screen mode.
        amt = (screen != nullptr) ? screen->mode() == SM_STANDARD ? amt : -amt : amt;
        travelTo(Transform(*transform).setRotation(amt));
    }

    float Turtle::towards(int x, int y){
        float amt = std::atan2(static_cast<float>(y) - transform->getTranslateY(), static_cast<float>(x) - transform->getTranslateX());
        
        if(toDegrees(amt) < 0){
            amt = 6.28319f - (-amt);
        }
        
        //convert to degrees if necessary.
        amt = state->angleMode ? amt : toDegrees(amt);
        return amt + heading();
    }
 
    void Turtle::goTo(int x, int y) {//had to change due to C++ keyword "goto"
        travelTo(Transform(*transform).setTranslation(x, y));
    };

    void Turtle::setx(int x) {
        travelTo(Transform(*transform).setTranslationX(x));
    }

    void Turtle::sety(int y) {
        travelTo(Transform(*transform).setTranslationY(y));
    }

    void Turtle::shift(int x, int y) {
        travelTo(Transform(*transform).translate(x, y));
    }

    void Turtle::home() {
        travelTo(Transform());
    }

    //Drawing & Misc.

    void Turtle::reset() {
        //Reset objects, transforms, trace lines, state, etc.

        //Note to self, clearing the list, appending a new transform,
        //then reassigning the transform reference just didn't want to work.
        //I have no idea why. Therefore, we're resetting it in the same
        //manner we initially construct it.
        stateStack = {PenState()};
        state = &stateStack.back();

        transform = &state->transform;
        const auto numItems = objects.size();

        if (screen != nullptr) {
            //Re-assign cursor on reset, derived from parent screen.
            state->cursor.reset(screen->shape("indented triangle").copy());
            //Erase all objects
            while (!objects.empty()) {
                screen->getScene().erase(objects.front());
                objects.pop_front();
            }

            //Alter cursor tilt and default transform
            //when operating under SM_LOGO mode.
            //This is to bring it up-to-par with Python's
            //implementation of screen modes.
            //I can't decide if this solution is too "hacky" or not;
            //it solves the problem, but I could have done it differently.
            if (screen->mode() == SM_LOGO) {
                state->cursorTilt = (-1.5708f);
                transform->rotate(1.5708f);
            }
        }

        updateParent(numItems > 0, false);
    }

    //Conditional parent update.

    void Turtle::updateParent(bool invalidate, bool input) {
        if (screen != nullptr)
            screen->update(invalidate, input);
    }

    void Turtle::circle(int radius, int steps, Color color) {
        pushGeom(*transform, new Circle(radius, steps, color));
        updateParent();
    }

    void Turtle::fill(bool val) {
        if (state->filling && !val) {
            //Add the fill polygon
            screen->getScene().emplace_back(new Polygon(fillAccum.points, state->fillColor), Transform());
            objects.push_back(std::prev(screen->getScene().end(), 1));

            //Add all trace lines created when tracing out the fill polygon.
            if (!fillLines.empty()) {
                for (auto& lineInfo : fillLines) {
                    screen->getScene().emplace_back(lineInfo.copy(), Transform());
                    objects.push_back(std::prev(screen->getScene().end(), 1));
                }
                fillLines.clear();
            }

            fillAccum.points.clear();
            updateParent(false, false);
            //trace line geometry in the screen's scene list.
        }
        state->filling = val;
    }

    void Turtle::draw(const Transform& screen, Image& canvas) {
        if (this->screen == nullptr || (!state->visible && !state->tracing))
            return;

        if (state->visible) {
            //Draw all lines queued during filling a shape.
            //This is only populated when the turtle moves between a beginfill
            //and endfill while the pen is down.
            for (const Line& line : fillLines)
                line.draw(screen, canvas);

            if (traveling && state->tracing) {
                //Draw the "Travel-Line" when in the middle of the travelTo func
                travelPoints[0] = screen(travelPoints[0]);
                travelPoints[1] = screen(travelPoints[1]);
                drawLine(canvas, travelPoints[0].x, travelPoints[0].y, travelPoints[1].x, travelPoints[1].y, state->penColor, state->penWidth);
            }

            //Add the extra rotate to start cursor facing right :)
            const float cursorRot = this->screen->mode() == SM_STANDARD ? 1.5708f : -3.1416f;
            Transform cursorTransform = screen.copyConcatenate(*transform).rotate(cursorRot + state->cursorTilt);
            state->cursor->fillColor = state->fillColor;
            state->cursor->outlineWidth = 1;
            state->cursor->outlineColor = state->penColor;
            state->cursor->draw(cursorTransform, canvas);
        }
    }

    bool Turtle::undo(bool try_redraw) {
        //total objects on the state stack prior to
        const unsigned long int totalBefore = state->objectsBefore;

        if (stateStack.size() >= 2)
            travelBack(); //Travel back if stack size >= 2

        //If we can't pop the state, break early.
        //TODO: Remove features as they're undone, rather than at the end of the traveling animation.
        if (!popState()) {
            return false;
        }

        auto begin = std::prev(objects.end(), (totalBefore - state->objectsBefore));
        auto iter = begin;

        while (iter != objects.end()) {
            screen->getScene().erase(*iter);
            iter++;
        }

        objects.erase(begin, objects.end());

        //Will invalidate the whole screen due to object removal, but we allow the option to not.
        updateParent(try_redraw, false);
        return true;
    }

    void Turtle::tilt(float amt) {
        amt = state->angleMode ? amt : toRadians(amt);
        //Flip angle orientation based on screen mode.
        amt = screen->mode() == SM_STANDARD ? amt : -amt;
        pushState();
        state->cursorTilt += amt;
        updateParent(false, false);
    }

    void Turtle::setshowturtle(bool val) {
        pushState();
        state->visible = val;
        updateParent(false, false);
    }

    void Turtle::setpenstate(bool down) {
        pushState();
        state->tracing = down;
    }

    void Turtle::travelBetween(Transform src, const Transform& dest, bool doPushState){
        if(dest == src)
            return;

        //Set the "traveling" state for screen drawing. Indicates when to draw travel lines (e.g, when pen is down).
        traveling = true;

        const float duration = static_cast<float>(getAnimMS());
        if ((screen != nullptr ? !screen->isclosed() : false) && duration > 0) {//no point in animating with no screen
            const unsigned long startTime = detail::epochTime();

            float progress = 0;
            while (progress < 1.0f) {
                //We use the time between animation frames to smooth out
                //our animations, making them take the same amount of time
                //regardless of how it's performance.
                const unsigned long curTime = detail::epochTime();

                transform->assign(src.lerp(dest, progress));
                travelPoints[0] = src.getTranslation();
                travelPoints[1] = transform->getTranslation();

                updateParent(false, false);

                progress = (static_cast<float>(curTime - startTime) / duration);
            }
        }

        if(doPushState){
            if (state->tracing && !state->filling) {
                pushTraceLine(src.getTranslation(), dest.getTranslation());
            } else if (state->filling) {
                fillAccum.points.push_back(dest.getTranslation());
                if (state->tracing) {
                    fillLines.push_back({src.getTranslation(), dest.getTranslation(), state->penColor, state->penWidth});
                }
            }

            transform->assign(src);
            pushState();
        }

        transform->assign(dest);
        traveling = false;
        updateParent(false, false);
    }

    void Turtle::pushState() {
        if (stateStack.size() + 1 > undoStackSize)
            stateStack.pop_front();

        stateStack.push_back(stateStack.back()); //Push a copy of the back-most pen state.
        state = &stateStack.back();
        transform = &state->transform;
        state->objectsBefore = objects.size();
    }

    bool Turtle::popState() {
        if (stateStack.size() == 1)
            return false;
        stateStack.pop_back();
        state = &stateStack.back();
        transform = &state->transform;
        return true;
    }

    bool Turtle::pushGeom(const Transform& t, AbstractDrawableObject* geom) {
        if (screen != nullptr) {
            pushState();
            screen->getScene().emplace_back(geom, t);
            objects.push_back(std::prev(screen->getScene().end()));
            return true;
        }
        return false;
    }

    bool Turtle::pushStamp(const Transform& t, AbstractDrawableObject* geom) {
        if (screen != nullptr) {
            pushState();
            const float cursorRot = this->screen->mode() == SM_STANDARD ? 1.5708f : -3.1416f;

            Transform trans(t);
            trans.rotate(cursorRot + state->cursorTilt);

            geom->outlineWidth = 1;
            geom->outlineColor = state->penColor;

            screen->getScene().emplace_back(geom, trans, state->curStamp++);
            SceneObject& obj = screen->getScene().back();

            objects.push_back(std::prev(screen->getScene().end()));
            return true;
        }
        return false;
    }

    bool Turtle::pushText(const Transform& t, Color color, const std::string& text) {
        if (screen != nullptr) {
            pushState();
            screen->getScene().emplace_back(new Text(text, color), t);
            objects.push_back(std::prev(screen->getScene().end()));
            return true;
        }
        return false;
    }

    bool Turtle::pushTraceLine(Point a, Point b) {
        if (screen != nullptr) {
            screen->getScene().emplace_back(new Line(a, b, state->penColor, state->penWidth), Transform());
            objects.push_back(std::prev(screen->getScene().end()));
            //Trace lines do NOT push a state->
            //Their state is encompassed by movement,
            //and these lines are only added when moving the turtle
            //while the pen is down.
            return true;
        }
        return false;
    }
}
