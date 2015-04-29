/* FEEDBACK:
 - peräkkäiset rivit yhdistetään blokeiksi
 - etsitään LIS jossa eniten peräkkäisiä rivejä
 - värjätään LIS:n inverse punaiseksi, blokeista ehkä vain tausta
 - sisennyspalaute kuten nykyisin alusta asti oikealla paikalla olevista riveistä (värjätäänkö vihreiksi?)
*/

// Takes an iterable sequence and returns the decks given by
// patience sorting as a list of lists
// http://wordaligned.org/articles/patience-sort
// http://en.wikipedia.org/wiki/Longest_increasing_subsequence

var LIS = {};

(function($, _) { // wrap in anonymous function to allow overriding of _ and $

  LIS.patience_sort = function(list) {
    var arr = _.toArray(list),
        decks = [[arr[0]]],
        deckPos = 0;
    for (var i = 1; i < arr.length; i++) {
      var x = arr[i],
          currDeck = decks[deckPos];
      if (x < _.last(currDeck)) {
        // append to the last created deck
        currDeck.push(x);
      } else {
        // create a new deck
        decks.push([x]);
        deckPos++;
      }
    }
    return decks;
  };

  // Takes an iterable sequence of iterables that represent decks
  // that are the result of patience sorting a sequence
  LIS.find_lises = function(decks) {
    decks = _.toArray(decks);
    if (decks.length < 1) {
      return decks;
    }
    var lises = [],
        new_lises,
        deck,
        partial_lis,
        partial_lis_extended,
        x, i, j, k;
    for (i = 0; i < decks.length; i++) {
      new_lises = [];
      deck = decks[i];
      for (j = 0; j < lises.length; j++) {
        partial_lis = lises[j];
        for (k = 0; k < deck.length; k++) {
          x = deck[k];
          if (x > _.last(partial_lis)) {
            new_partial_lis = partial_lis.slice(0); // dummy copy
            new_partial_lis.push(x);
            new_lises.push(new_partial_lis);
          }
        }
        new_lises.push(partial_lis);
      }
      for (k = 0; k < deck.length; k++) {
        new_lises.push([deck[k]]);
      }
      lises = new_lises;
    }
    lis_length = _.max(_.map(lises, function(item) { return item.length; }));
    lises = _.select(lises, function(item) { return item.length >= lis_length; });
    return lises;
  };

  LIS.best_lise = function(lises) {
    var lis_scores = _.map(lises, function(item, index) {
      if (item.length <= 1) {
        return {score: 0, index: index};
      }
      var score = 0;
      for (var i = 1; i < item.length; i++) {
        if (item[i-1] == item[i] - 1) {
          score++;
        }
      }
      return {score: score, index: index};
    });
    var best = _.max(lis_scores, function(item) { return item.score; });
    return lises[best.index];
  };

  LIS.best_lise_inverse = function(list) {
    var decks = this.patience_sort(_.toArray(list)),
        lises = this.find_lises(decks),
        best = this.best_lise(lises);
    return _.difference(list, best);
  };

// Takes an iterable sequence and returns a list of the inverses of
// all the longest increasing subsequences of this sequence
/*
function lis_inverses(list) {
  var inverse_list = [],
      decks = patience_sort(_.toArray(list)),
      lises = find_lises(decks);
  return _.map(lises, function(item) { return _.difference(list, item); });
}

function in_all_lis_inverses(list) {
  var inverse_list = lis_inverses(list);
  return _.intersection.apply(null, inverse_list);
}

function inverse_indices(list) {
  var in_all = in_all_lis_inverses(list);
  return _.map(in_all, function(item) { return list.indexOf(item); });
};*/

//This allows the current version of _ and $ to be used, even if it is later reverted
//with noConflict
})($, _);
