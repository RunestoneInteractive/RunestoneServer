// from ipython/docs/examples/notebooks/OPT.ipynb
var json = {
        "code": "\ndef fact(n):\n    if (n <= 1):\n        return 1\n    else:\n        return n * fact(n - 1)\n\nprint(fact(6))",
        "trace": [
         {
          "event": "step_line",
          "func_name": "<module>",
          "globals": {},
          "heap": {},
          "line": 2,
          "ordered_globals": [],
          "stack_to_render": [],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "<module>",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 8,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [],
          "stdout": ""
         },
         {
          "event": "call",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 2,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           }
          ],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 3,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           }
          ],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 6,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           }
          ],
          "stdout": ""
         },
         {
          "event": "call",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 2,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           }
          ],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 3,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           }
          ],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 6,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           }
          ],
          "stdout": ""
         },
         {
          "event": "call",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 2,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           }
          ],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 3,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           }
          ],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 6,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           }
          ],
          "stdout": ""
         },
         {
          "event": "call",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 2,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           },
           {
            "encoded_locals": {
             "n": 3
            },
            "frame_id": 4,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f4"
           }
          ],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 3,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           },
           {
            "encoded_locals": {
             "n": 3
            },
            "frame_id": 4,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f4"
           }
          ],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 6,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           },
           {
            "encoded_locals": {
             "n": 3
            },
            "frame_id": 4,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f4"
           }
          ],
          "stdout": ""
         },
         {
          "event": "call",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 2,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           },
           {
            "encoded_locals": {
             "n": 3
            },
            "frame_id": 4,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f4"
           },
           {
            "encoded_locals": {
             "n": 2
            },
            "frame_id": 5,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f5"
           }
          ],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 3,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           },
           {
            "encoded_locals": {
             "n": 3
            },
            "frame_id": 4,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f4"
           },
           {
            "encoded_locals": {
             "n": 2
            },
            "frame_id": 5,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f5"
           }
          ],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 6,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           },
           {
            "encoded_locals": {
             "n": 3
            },
            "frame_id": 4,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f4"
           },
           {
            "encoded_locals": {
             "n": 2
            },
            "frame_id": 5,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f5"
           }
          ],
          "stdout": ""
         },
         {
          "event": "call",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 2,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           },
           {
            "encoded_locals": {
             "n": 3
            },
            "frame_id": 4,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f4"
           },
           {
            "encoded_locals": {
             "n": 2
            },
            "frame_id": 5,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f5"
           },
           {
            "encoded_locals": {
             "n": 1
            },
            "frame_id": 6,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f6"
           }
          ],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 3,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           },
           {
            "encoded_locals": {
             "n": 3
            },
            "frame_id": 4,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f4"
           },
           {
            "encoded_locals": {
             "n": 2
            },
            "frame_id": 5,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f5"
           },
           {
            "encoded_locals": {
             "n": 1
            },
            "frame_id": 6,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f6"
           }
          ],
          "stdout": ""
         },
         {
          "event": "step_line",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 4,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           },
           {
            "encoded_locals": {
             "n": 3
            },
            "frame_id": 4,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f4"
           },
           {
            "encoded_locals": {
             "n": 2
            },
            "frame_id": 5,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f5"
           },
           {
            "encoded_locals": {
             "n": 1
            },
            "frame_id": 6,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f6"
           }
          ],
          "stdout": ""
         },
         {
          "event": "return",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 4,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           },
           {
            "encoded_locals": {
             "n": 3
            },
            "frame_id": 4,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f4"
           },
           {
            "encoded_locals": {
             "n": 2
            },
            "frame_id": 5,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f5"
           },
           {
            "encoded_locals": {
             "__return__": 1,
             "n": 1
            },
            "frame_id": 6,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n",
             "__return__"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f6"
           }
          ],
          "stdout": ""
         },
         {
          "event": "return",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 6,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           },
           {
            "encoded_locals": {
             "n": 3
            },
            "frame_id": 4,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f4"
           },
           {
            "encoded_locals": {
             "__return__": 2,
             "n": 2
            },
            "frame_id": 5,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n",
             "__return__"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f5"
           }
          ],
          "stdout": ""
         },
         {
          "event": "return",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 6,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           },
           {
            "encoded_locals": {
             "__return__": 6,
             "n": 3
            },
            "frame_id": 4,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n",
             "__return__"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f4"
           }
          ],
          "stdout": ""
         },
         {
          "event": "return",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 6,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           },
           {
            "encoded_locals": {
             "__return__": 24,
             "n": 4
            },
            "frame_id": 3,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n",
             "__return__"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f3"
           }
          ],
          "stdout": ""
         },
         {
          "event": "return",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 6,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": false,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           },
           {
            "encoded_locals": {
             "__return__": 120,
             "n": 5
            },
            "frame_id": 2,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n",
             "__return__"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f2"
           }
          ],
          "stdout": ""
         },
         {
          "event": "return",
          "func_name": "fact",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 6,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [
           {
            "encoded_locals": {
             "__return__": 720,
             "n": 6
            },
            "frame_id": 1,
            "func_name": "fact",
            "is_highlighted": true,
            "is_parent": false,
            "is_zombie": false,
            "ordered_varnames": [
             "n",
             "__return__"
            ],
            "parent_frame_id_list": [],
            "unique_hash": "fact_f1"
           }
          ],
          "stdout": ""
         },
         {
          "event": "return",
          "func_name": "<module>",
          "globals": {
           "fact": [
            "REF",
            1
           ]
          },
          "heap": {
           "1": [
            "FUNCTION",
            "fact(n)",
            null
           ]
          },
          "line": 8,
          "ordered_globals": [
           "fact"
          ],
          "stack_to_render": [],
          "stdout": "720\n"
         }
        ]
       };


$(document).ready(function() {
        // simulate behavior of ipython/IPython/frontend/html/notebook/static/js/outputarea.js

        console.log(json);
        var toinsert = $("<div/>").attr('id','optviz');
        $('.output_area').append(toinsert);
        var viz = new ExecutionVisualizer(toinsert, json, {embeddedMode: true});
        console.log(viz);
        $(window).resize(function() {
          viz.redrawConnectors();
        });
});
