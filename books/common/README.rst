All of the common files needed by extensions are here:   All this gets copied to the static/<mybook>/_static folder when sphinx is run.

bootstrap:   images/*   -- these are all of the images used by the bootstrap theme  The images subfolder is there because the bootsrap theme expects to find all of its images in _static/images

js  -- javascript files for all of the runestone extensions are here, as well as jquery and other requirements

css -- all of the css files

images -- This is for misc images not associated with bootstrap that should end up in the _static folder

ext -- This contains the submodules that are used by the sphinx directives currently

* skulpt -- only skulpt/dist/*.js gets copied to the _static folder
* js-parsons -- everything under js-parsons ends up in _static
* codelens  -- everything under codelens/v3 ends up in _static

