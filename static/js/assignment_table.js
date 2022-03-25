// *************************************
// |docname| -- Assignment table support
// *************************************
// This code operates on the assignment table created in the grading tab of the instructor interface.
//
//
// Assignment table
// ================
// Both the grouped assignment table and the assignment table have, at their heart, a grade (a collection of items -- timestamp, answer, etc.). However, a traditional spreadsheet only displays one item per cell. To make this possible, this code must:
//
// #.   Provide a ``Grade`` class to contain each cell's information.
// #.   For the filter to work, provide a ``toString`` that returns the answer, since that's the mostly likely item for users to filter on.
// #.   For edits to the table to work, provide a ``GradeEditor`` which selects the score to be edited (the only editable item). Also provide a way to translate a grade to a score for the validator (the ``beforeValidate`` key/value).
// #.   To allow display of the components of the grade, a ``gradeRenderer`` which produces HTML for the enabled grade components.
//
// However, the tables contains more than just grades -- there's also user and question info, along with row and column headings. Therefore, the ``cell`` key/value pair provides a function to assign the correct properties (editablity, formatting, etc.) to all these types of cells.
//
// The assignment table shape is:
/// column    0                1            2         3          4      5
/// row     userid        family name  given name  e-mail   avg grade  Q-1...
///  0      div_id        text         text        text     text       text
///  1      location      text         text        text     text       text
///  2      type          text         text        text     text       text
///  3      points        text         text        text     text       number
///  4      avg grade     text         text        text     text       number
///  5      avg attempts  text         text        text     text       number
///  6      userid 1...   text         text        text     number     grade
//
//
// Common variables
// ----------------
// Visibility options for a cell in the assingment table: the assignment table cell visibility (atcv).
const atcv = {
    TIMESTAMP: 1,
    SCORE: 2,
    ANSWER: 4,
    CORRECT: 8,
    CORRECT_SHADING: 16,
    ATTEMPTS: 32,
};

// The assignment table row headers.
const atrh = {
    DIV_ID: 0,
    LOCATION: 1,
    TYPE: 2,
    POINTS: 3,
    AVG_GRADE: 4,
    AVG_ATTEMPTS: 5,
};

// The assignment table column headers.
const atch = {
    USERID: 0,
    FAMILY_NAME: 1,
    GIVEN_NAME: 2,
    E_MAIL: 3,
    AVG_GRADE: 4,
};

// Current visibility state.
var assignment_table_cell_visibility = atcv.ANSWER | atcv.CORRECT_SHADING;

// The assignment table object.
var assignment_table = null;

// Create a class to produce a helpful ``toString`` result for each grade. The filter plugin operates based on this value.
class Grade {
    constructor(
        // The array of grade values passed from the server: timestamp (as a string), score, answer, correct, attempts.
        grade_array
    ) {
        this.timestamp = new Date(grade_array[0]);
        [this.score, this.answer, this.correct, this.attempts] = grade_array.slice(1);
    }

    toString() {
        return this.answer ? this.answer.toString() : "";
    }
}

// A custom editor for this class which selects the score to be edited from a Grade, then places the edited value back in a Grade.
class GradeEditor extends Handsontable.editors.NumericEditor {
    prepare(row, col, prop, td, originalValue, cellProperties) {
        // Invoke the original method.
        super.prepare(row, col, prop, td, originalValue, cellProperties);
        // Set the score (if it exists) as the object to edit.
        if (this.originalValue) {
            this.originalValue = this.originalValue.score;
        }
    }

    // Given a new score, save this back into the Grade class.
    saveValue(value, ctrlDown) {
        // The value to save is a 2-D array of ``[[single_value]]``, probably to make internals easier to use (see the ``_baseEditor.saveValue``, which calls ``populatefromArray``, which expects a 2-D array).
        let single_value = value[0][0];
        let grade = this.hot.getDataAtCell(this.row, this.col);
        if (grade) {
            // Don't edit the old grade -- it needs to stay unchanged if the validator wants to revert back to it. Instead, create a new instance.
            grade = new Grade([
                grade.timestamp,
                single_value,
                grade.answer,
                grade.correct,
                grade.attempts,
            ]);
        } else {
            grade = new Grade(null, single_value, null, null);
        }
        // Repack the grade into a 2-D array. Don't allow multiple edits by passing ``false`` for ``ctrlDown`` (ctrl+enter in Excel evidently applies the same entry to all selected cells). TODO: this could be implemented, but who would use it?
        super.saveValue([[grade]], false);
    }
}

// Table creation
// --------------
// This is called by the when data for the assignment table is received.
function populateAssignmentTable() {
    // Show the loading message.
    $(".assigment_table_buttons").show();
    $("#assignment_info_table_loading").show();

    // If rows/cols have been hidden, remember those before removing the table.
    let hiddenRows = [];
    let hiddenColumns = [];
    if (assignment_table) {
        // WARNING: These aren't documented!
        hiddenRows = assignment_table.getPlugin("hiddenRows").hiddenRows;
        hiddenColumns = assignment_table.getPlugin("hiddenColumns").hiddenColumns;

        // Clear any previous contents.
        assignment_table.destroy();
    }

    let old_assignment_table = assignment_table;
    assignment_table = null;
    $("#assignment_info_table").show();

    // Clear the grouped assignments, since it refers to an older version of this table.
    if (grouped_assignment_table) {
        grouped_assignment_table.destroy();
    }
    grouped_assignment_table = null;
    $("#grouped_assignment_info_table").hide();

    // Update the assignment table for this assignment.
    $.getJSON(
        "../assignments/grades_report",
        {
            report_type: $("#gradingoption1").val(),
            chap_or_assign: $("#chaporassignselector").val(),
        },
        (data) => {
            // Check for errors.
            if ("errors" in data) {
                $("#assignment_info_table_loading").html(
                    `Error<br/>Please report this error: ${escapeHTML(data.errors)}`
                );
                return;
            }

            // Recreate more helpful data structures from the "flattened" data.
            data.orig_data.forEach((user_id_row, user_id_index) =>
                user_id_row.forEach((div_id_entry, div_id_index) => {
                    if (div_id_entry) {
                        data.data[user_id_index + 6][div_id_index + 5] = new Grade(
                            div_id_entry
                        );
                    }
                })
            );

            // The data
            let hot_data = {
                filters: true,
                dropdownMenu: [
                    "alignment",
                    "filter_by_condition",
                    "filter_operators",
                    "filter_by_condition2",
                    "filter_by_value",
                    "filter_action_bar",
                ],
                manualColumnResize: true,
                height: "70vh",
                licenseKey: "non-commercial-and-evaluation",
                hiddenRows: {
                    indicators: true,
                    rows: hiddenRows,
                },
                hiddenColumns: {
                    indicators: true,
                    columns: hiddenColumns,
                },
                // Freeze userid, last name, first name, e-mail address, and avg grade.
                fixedColumnsLeft: 5,
                // Freeze top stuff.
                fixedRowsTop: 6,

                // See https://handsontable.com/docs/7.2.2/PersistentState.html.
                persistentState: true,

                // Don't allow invalid edits
                allowInvalid: false,

                // Change the Grade into a score before the Validator sees it.
                beforeValidate: function (value, row, prop, source) {
                    return value.score;
                },

                // Don't allow trimming (from the filter) a row heading.
                beforeTrimRow: function (
                    currentTrimConfig,
                    destinationTrimConfig,
                    actionPossible
                ) {
                    new_destinationTrimConfig = destinationTrimConfig.filter(
                        (row) => row > atrh.AVG_ATTEMPTS
                    );
                    // A hack to filter the array in place, since we need to alter what rows are being trimmed.
                    destinationTrimConfig.splice(
                        0,
                        destinationTrimConfig.length,
                        ...new_destinationTrimConfig
                    );
                },

                // Update averages after a trim.
                afterTrimRow: function (currentTrimConfig, destinationTrimConfig) {
                    computeAssignmentTableAverages();
                    $("#assignment_table_students").val(destinationTrimConfig);
                },

                // Define cell properties.
                cells: function (row, column, prop) {
                    // The expression referrs to all pure text in the table.
                    if (
                        row <= atrh.TYPE ||
                        column <= atch.E_MAIL ||
                        (row <= atrh.AVG_ATTEMPTS && column <= atch.AVG_GRADE)
                    ) {
                        return {
                            renderer: function (
                                instance,
                                td,
                                row,
                                col,
                                prop,
                                value,
                                cellProperties
                            ) {
                                // A special case: headings for columns, which should appear on the first shown column.
                                if (row <= atrh.AVG_ATTEMPTS && col <= atch.AVG_GRADE) {
                                    // Get a list of hidden columns, in sorted order.
                                    let hc = instance
                                        .getPlugin("hiddenColumns")
                                        .hiddenColumns.slice()
                                        .sort();
                                    // Col should be the title if:
                                    // -    col not in hc
                                    // -    all numbers < col are in hc
                                    if (
                                        !hc.includes(col) &&
                                        JSON.stringify([0, 1, 2, 3, 4].slice(0, col)) ===
                                            JSON.stringify(hc.slice(0, col))
                                    ) {
                                        td.style.fontWeight = "bold";
                                        // Get the title, in case this isn't column 0 (where the titles are stored).
                                        value = instance.getDataAtCell(row, 0);
                                    }
                                }
                                Handsontable.renderers.TextRenderer.apply(
                                    this,
                                    arguments
                                );
                            },
                            type: "text",
                            editor: false,
                        };
                        // Failing the above, pick out all numbers in the table.
                    } else if (row == atrh.POINTS || row == atrh.AVG_ATTEMPTS) {
                        return {
                            type: "numeric",
                            numericFormat: {
                                pattern: "0.0",
                            },
                            editor: false,
                        };
                        // Failing that, pick out percentages.
                    } else if (row == atrh.AVG_GRADE || column == atch.AVG_GRADE) {
                        return {
                            type: "numeric",
                            numericFormat: {
                                pattern: "0.0%",
                            },
                            editor: false,
                        };
                        // Everything else is grade cells.
                    } else {
                        return {
                            renderer: gradeRenderer,
                            validator: "numeric",
                            // Only allow editing if the score is shown and editing is enabled.
                            editor:
                                assignment_table_cell_visibility & atcv.SCORE &&
                                $("#allow_editing_scores").is(":checked")
                                    ? GradeEditor
                                    : false,
                        };
                    }
                },

                afterChange: function (changes, source) {
                    // See https://handsontable.com/docs/7.2.2/tutorial-using-callbacks.html?_ga=2.207032341.727290537.1573772747-250672174.1568901849#page-source-definition.
                    if (source === "edit") {
                        changes.forEach(([row, prop, oldValue, newValue]) => {
                            // The grade is a string -- fix that. Change an empty string into a null, which will erase the current grade.
                            newValue.score =
                                newValue.score.trim() === ""
                                    ? null
                                    : parseFloat(newValue.score);
                            // TODO: warn the user if this fails.
                            $.post("../assignments/record_grade", {
                                // The ``sid`` is the userid. Get it from the table.
                                sid: assignment_table.getDataAtCell(row, atch.USERID),
                                // The ``acid`` is the div_id. Get it from the table. The ``prop`` is actually the column.
                                acid: assignment_table.getDataAtCell(atrh.DIV_ID, prop),
                                // The name of the assignment.
                                assignmentid: $("#chaporassignselector").val(),

                                grade: newValue.score,
                                comment: "Manually graded",
                            });
                        });

                        computeAssignmentTableAverages();
                    }
                },
            };

            let container = document.getElementById("assignment_info_table");
            // Use Object.assign to merge two dicts.
            assignment_table = new Handsontable(
                container,
                Object.assign({}, data, hot_data)
            );
            computeAssignmentTableAverages();

            // Add students to the student selector.
            let student_select2 = $("#assignment_table_students");
            student_select2.empty();
            data.data.slice(6).forEach(function (row, row_index) {
                student_select2.append(
                    new Option(
                        row[atch.GIVEN_NAME] + " " + row[atch.FAMILY_NAME],
                        row_index + 6,
                        false,
                        false
                    )
                );
            });
            student_select2.trigger("change");

            // Update select2 boxes the first time the assignment table is created, so their checked items will be synced with the table.
            if (!old_assignment_table) {
                assignmentTableShowRows($("#assignment_table_rows_visibility"));
                assignmentTableShowColumns($("#assignment_table_columns_visibility"));
                assignmentTableShowCells($("#assignment_table_cells_visibility"));
            }

            // Hide the loading message now that we're done.
            $("#assignment_info_table_loading").hide();

            // Group answers if requested.
            if ($("#group_identical_answers").is(":checked")) {
                groupIdenticalAnswers(true);
            }
        }
    );
}

// Compute averages for each column.
function computeAssignmentTableAverages() {
    let data = assignment_table.getData();
    let num_students = data.length - 5;
    let new_averages = [];
    if (num_students === 0) {
        return;
    }
    // Walk through each question (questions start at index 5).
    for (let column_index = 5; column_index < data[0].length; ++column_index) {
        let total_grade = 0;
        let total_attempts = 0;
        // Sum these values over all rows in this column.
        for (let row_index = 6; row_index < data.length; ++row_index) {
            let grade = data[row_index][column_index];
            if (grade) {
                total_grade += grade.score;
                total_attempts += grade.attempts;
            }
        }

        // Store the averages.
        let max_points = data[atrh.POINTS][column_index];
        new_averages.push([
            atrh.AVG_GRADE,
            column_index,
            total_grade / (num_students * max_points),
        ]);
        new_averages.push([
            atrh.AVG_ATTEMPTS,
            column_index,
            total_attempts / num_students,
        ]);
    }

    // Save the new averages.
    assignment_table.setDataAtCell(new_averages, null, null, "average calculator");
}

// Cell rendering
// --------------
// The many different types of questions, and different types of data in a grade need renderers to transform them into the appropriate HTML.
//
// Grade rendering
// ^^^^^^^^^^^^^^^
// Render one grade cell in the assignment table.
function gradeRenderer(instance, td, row, col, prop, value, cellProperties) {
    // Make the cell's background red if the answer isn't correct.
    if (
        assignment_table_cell_visibility & atcv.CORRECT_SHADING &&
        (!value || !value.correct)
    ) {
        // A light red.
        td.style.background = "#ffcccc";
    }

    // Select what to display
    let displayed_value = "";
    if (value) {
        displayed_value = [];
        if (assignment_table_cell_visibility & atcv.TIMESTAMP) {
            displayed_value.push(value.timestamp.toLocaleString());
        }
        if (assignment_table_cell_visibility & atcv.ANSWER) {
            let question_type = instance.getDataAtCell(2, col);
            displayed_value.push(renderAnswer(question_type, value.answer));
        }
        let more_displayed_value = renderScoreCorrect(value);
        if (assignment_table_cell_visibility & atcv.ATTEMPTS) {
            more_displayed_value.push(
                '<span style="color: green">' + value.attempts + "</span>"
            );
        }
        if (more_displayed_value.length) {
            displayed_value.push(more_displayed_value.join(" "));
        }
        displayed_value = displayed_value.join("<br/>");
    }

    Handsontable.renderers.HtmlRenderer(
        instance,
        td,
        row,
        col,
        prop,
        displayed_value,
        cellProperties
    );
}

// Produce a nicely-formatted answer, in HTML.
function renderAnswer(question_type, answer) {
    if (!answer) {
        return "(unanswered)";
    }
    if (question_type === "lp_build") {
        return isEmpty(answer)
            ? ""
            : // TODO: Make this a style.
              '<div style="max-width: 30rem; max-height: 18.5rem; overflow: auto">' +
                  "<p>code_snippets:<br />" +
                  '<span style="white-space: pre"><code>' +
                  escapeHTML(answer.code_snippets.toString()) +
                  "</code></span></p>" +
                  "<p>resultString:<br />" +
                  '<span style="white-space: pre"><code>' +
                  escapeHTML(answer.resultString) +
                  "</code></span></p>" +
                  "</div>";
    } else if (question_type === "mchoice") {
        // Convert the number reperesenting each multiple choie answer to the corresponding letter.
        return answer
            .map((ans) => String.fromCharCode("A".charCodeAt() + ans))
            .join(", ");
    } else {
        // TODO: Include more renderers for each question type.
        return escapeHTML(answer.toString());
    }
}

// Render the score and correct fields, returning an array of strings.
function renderScoreCorrect(value) {
    let more_displayed_value = [];
    if (assignment_table_cell_visibility & atcv.SCORE) {
        more_displayed_value.push(
            '<span style="color: blue">' +
                (value.score === null ? "" : value.score) +
                "</span>"
        );
    }
    if (assignment_table_cell_visibility & atcv.CORRECT) {
        more_displayed_value.push(
            value.correct === true
                ? '<span style="color: green">✔</span>'
                : value.correct === false
                ? '<span style="color: red">✖</span>'
                : value.correct
        );
    }

    return more_displayed_value;
}

// Utilities
// ^^^^^^^^^
// Given text, escape it so it formats correctly as HTML. Taken from https://stackoverflow.com/a/48054293. Note that this also transforms newlines into <br> -- see https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/innerText.
function escapeHTML(unsafeText) {
    let div = document.createElement("div");
    div.innerText = unsafeText;
    return div.innerHTML;
}

// Determine if a dict/object is empty. Taken from a comment in https://coderwall.com/p/_g3x9q/how-to-check-if-javascript-object-is-empty.
function isEmpty(o) {
    return !Object.keys(o).length;
}

// Handle clicks from the assignment table select2 boxes
// =====================================================
function assignmentTableShowRows(sel) {
    [assignment_table, grouped_assignment_table].forEach(function (table) {
        if (table) {
            let hr = table.getPlugin("hiddenRows");
            // Hide all rows.
            hr.hideRows([0, 1, 2, 3, 4, 5]);
            // Show selected rows.
            hr.showRows(($(sel).val() || []).map((o) => parseInt(o)));

            table.render();
        }
    });
}

function assignmentTableShowColumns(sel) {
    if (assignment_table) {
        let hr = assignment_table.getPlugin("hiddenColumns");
        // Hide all columns.
        hr.hideColumns([0, 1, 2, 3, 4]);
        // Show selected columns.
        hr.showColumns(($(sel).val() || []).map((o) => parseInt(o)));

        assignment_table.render();
    }
}

function assignmentTableShowCells(sel) {
    assignment_table_cell_visibility = 0;
    ($(sel).val() || []).forEach((o) => (assignment_table_cell_visibility |= atcv[o]));
    if (assignment_table) {
        assignment_table.render();
    }
    if (grouped_assignment_table) {
        grouped_assignment_table.render();
    }
}

function assignmentTableStudentVisibility(sel) {
    if (assignment_table) {
        let invisible_students = ($(sel).val() || []).map((o) => parseInt(o));
        let tr = assignment_table.getPlugin("trimRows");
        tr.untrimAll();
        tr.trimRows(invisible_students);
    }
}

function allowEditingScores(isChecked) {
    // TODO: add a warning dialog when this is checked the first time
    if (assignment_table) {
        assignment_table.render();
    }
}

// Set true when scores are changed in the grouped assignments table. This is used as a dirty flag to reload the assignment table before rendering it.
var grouped_scores_changed = false;

function groupIdenticalAnswers(isChecked) {
    let ait = $("#assignment_info_table");
    let gait = $("#grouped_assignment_info_table");
    let aci = $(".assignment_table_only");
    if (isChecked) {
        if (grouped_assignment_table) {
            // Update the contents, in case any scores were edited since the grouped assignment table was last built.
            buildGroupedAssignmentTable();
        } else {
            createGroupedAssignmentTable();
        }
        ait.hide();
        gait.show();
        // Disable the select2 box.
        aci.prop("disabled", true);
        // A convoluted way to disable options in a select2. Nothing else works.
        $("option.assignment_table_only").each(
            (idx, value) => ($(value).data("data").disabled = true)
        );

        // Since we just pulled data from the assignment table to create the grouped assignment table, no grouped scores have changed.
        grouped_scores_changed = false;

        grouped_assignment_table.render();
    } else {
        gait.hide();
        ait.show();
        aci.prop("disabled", false);
        $("option.assignment_table_only").each(
            (idx, value) => ($(value).data("data").disabled = false)
        );

        if (grouped_scores_changed) {
            populateAssignmentTable();
        } else {
            assignment_table.render();
        }
    }
}

// Grouped assignment table
// ========================
// The table format is:
//
/// column    0            1
/// row     userid        Q-1...
///  0      div_id        text
///  1      location      text
///  2      type          text
///  3      points        number
///  4      avg grade     percent
///  5      avg attempts  number
///  6      empty         grade

// The grouped assignment table object
var grouped_assignment_table = null;

// Take an existing assignment table and group identical answers.
function buildGroupedAssignmentTable() {
    let data = assignment_table.getData();
    // Copy the row headers only.
    let grouped_data = data.slice(0, 6);
    for (let row = 0; row < data.length; ++row) {
        // Keep only titles in the first 5 rows
        if (row < 6) {
            grouped_data[row] = [grouped_data[row][0]].concat(
                grouped_data[row].slice(5)
            );
        } else {
            // Create empty arrays for the max possible entries
            grouped_data[row] = [""];
        }
    }

    // Walk through each div_id (row 0) in the table, starting after the headers (column 6).
    let data_no_headers = data.slice(6);
    let max_answers_length = -1;
    data[0].slice(5).forEach((div_id, div_id_index) => {
        let answer_dict = {};
        data_no_headers.forEach((user_id_row, user_id_index) => {
            let grade = data[user_id_index + 6][div_id_index + 5];
            let answer = null;
            let score = null;
            let correct = null;
            if (grade) {
                answer = grade.answer;
                score = grade.score;
                correct = grade.correct;
            }
            // Encode the struct as JSON, since dict keys can't be an object/dict.
            answer = JSON.stringify(answer);
            // Append this user_id to the list of user_ids stored at key ``answer``.
            if (!(answer in answer_dict)) {
                answer_dict[answer] = {
                    user_ids: [],
                    score: score,
                    correct: correct,
                };
            }
            // Append the user_id (element 0 of the ``user_id_row``) to the list.
            let ad = answer_dict[answer];
            ad.user_ids.push(user_id_row[0]);
            // See if the score and correct are the same.
            if (score !== ad.score) {
                ad.score = "varies";
            }
            if (correct != ad.correct) {
                ad.correct = "varies";
            }
        });

        // Sort the resulting array by the number of user_ids in each key. The result of ``Object.entries`` is ``[ [key0, val0], [key1, val1], ... ]``, so that ``a[1]`` refers to the value.
        let sorted_answers = Object.entries(answer_dict).sort(
            (a, b) => b[1].user_ids.length - a[1].user_ids.length
        );

        // Add this to ``grouped_data``.
        sorted_answers.forEach((key_value, index) =>
            grouped_data[index + 6].push({
                // Transform the answer back into an object.
                answer: JSON.parse(key_value[0]),
                user_ids: key_value[1].user_ids,
                score: key_value[1].score,
                correct: key_value[1].correct,
            })
        );
        // Add padding to the bottom of ``grouped_data``.
        for (
            let index = 6 + sorted_answers.length;
            index < grouped_data.length;
            ++index
        ) {
            grouped_data[index].push(null);
        }

        // Update max
        max_answers_length = Math.max(max_answers_length, sorted_answers.length);
    });

    // Drop extra rows.
    return grouped_data.slice(0, 6 + max_answers_length);
}

// Create the grouped table.
function createGroupedAssignmentTable() {
    // Create the table.
    let container = document.getElementById("grouped_assignment_info_table");
    grouped_assignment_table = new Handsontable(container, {
        manualColumnResize: true,
        height: "70vh",
        licenseKey: "non-commercial-and-evaluation",
        // See https://handsontable.com/docs/7.2.2/Options.html#columns.

        // Copy these settings from the assignment table.
        colHeaders: [""].concat(assignment_table.getColHeader().slice(5)),
        // WARNING: this is undocumented.
        // TODO: Fix these up, by subtacting 5 from all row values.
        mergeCells: assignment_table
            .getPlugin("MergeCells")
            .mergedCellsCollection.mergedCells.map(function (mergeCell) {
                // Merged cells at column x in the assignment table should start at columnh x - 4 in this table, since it has fewer column headers.
                return Object.assign({}, mergeCell, { col: mergeCell.col - 4 });
            }),
        hiddenRows: {
            indicators: true,
            rows: assignment_table.getPlugin("hiddenRows").hiddenRows,
        },

        // Freeze top stuff.
        fixedRowsTop: 6,

        // See https://handsontable.com/docs/7.2.2/PersistentState.html.
        persistentState: true,

        // Don't allow invalid edits
        allowInvalid: false,

        // Change the Grade into a score before the Validator sees it.
        beforeValidate: function (value, row, prop, source) {
            return value.score;
        },

        data: buildGroupedAssignmentTable(),

        cells: function (row, column, prop) {
            // Text cells.
            if (row <= atrh.TYPE || column == 0) {
                return {
                    renderer: function (
                        instance,
                        td,
                        row,
                        col,
                        prop,
                        value,
                        cellProperties
                    ) {
                        // Make the column headings bold.
                        if (column === 0) {
                            td.style.fontWeight = "bold";
                        }
                        Handsontable.renderers.TextRenderer.apply(this, arguments);
                    },
                    type: "text",
                    editor: false,
                };
                // Number cells.
            } else if (row == atrh.POINTS || row == atrh.AVG_ATTEMPTS) {
                return {
                    type: "numeric",
                    numericFormat: {
                        pattern: "0.0",
                    },
                    editor: false,
                };
                // Percentage
            } else if (row == atrh.AVG_GRADE) {
                return {
                    type: "numeric",
                    numericFormat: {
                        pattern: "0.0%",
                    },
                    editor: false,
                };
                // Grades.
            } else {
                return {
                    renderer: groupedRenderer,
                    validator: "numeric",
                    // Only allow editing if the score is shown and editing is enabled, and only if there's a valid entry in this cell.
                    editor:
                        assignment_table_cell_visibility & atcv.SCORE &&
                        $("#allow_editing_scores").is(":checked") &&
                        grouped_assignment_table.getDataAtCell(row, column)
                            ? GroupedEditor
                            : false,
                };
            }
        },

        afterChange: function (changes, source) {
            // See https://handsontable.com/docs/7.2.2/tutorial-using-callbacks.html?_ga=2.207032341.727290537.1573772747-250672174.1568901849#page-source-definition.
            if (source === "edit") {
                changes.forEach(([row, prop, oldValue, newValue]) => {
                    // The grade is a string -- fix that. Change an empty string into a null, which will erase the current grade.
                    newValue.score =
                        newValue.score.trim() === "" ? null : parseFloat(newValue.score);
                    // TODO: warn the user if this fails.
                    $.post("../assignments/record_grade", {
                        // The ``sid`` is the userid. Pass a list of them.
                        sid: newValue.user_ids,
                        // The ``acid`` is the div_id. Get it from the table. The ``prop`` is actually the column.
                        acid: grouped_assignment_table.getDataAtCell(atrh.DIV_ID, prop),
                        // The name of the assignment.
                        assignmentid: $("#chaporassignselector").val(),

                        grade: newValue.score,
                        comment: "Manually graded",
                    });
                });

                computeAssignmentTableAverages();
                grouped_scores_changed = true;
            }
        },
    });
}

function groupedRenderer(instance, td, row, col, prop, value, cellProperties) {
    // Select what to display
    let displayed_value = "";
    if (value) {
        displayed_value = ["Count: " + value.user_ids.length];
        let question_type = instance.getDataAtCell(2, col);
        displayed_value.push(renderAnswer(question_type, value.answer));

        let more_displayed_value = renderScoreCorrect(value);
        if (more_displayed_value.length) {
            displayed_value.push(more_displayed_value.join(" "));
        }
        displayed_value = displayed_value.join("<br/>");

        // Make the cell's background red if the answer isn't correct.
        if (
            assignment_table_cell_visibility & atcv.CORRECT_SHADING &&
            (!value || !value.correct)
        ) {
            // A light red.
            td.style.background = "#ffcccc";
        }
    }

    Handsontable.renderers.HtmlRenderer(
        instance,
        td,
        row,
        col,
        prop,
        displayed_value,
        cellProperties
    );
}

// A custom editor for this class which selects the score to be edited from a Grade, then places the edited value back in a Grade.
class GroupedEditor extends Handsontable.editors.NumericEditor {
    prepare(row, col, prop, td, originalValue, cellProperties) {
        // Invoke the original method.
        super.prepare(row, col, prop, td, originalValue, cellProperties);
        // Set the score (if it exists) as the object to edit.
        if (this.originalValue) {
            this.originalValue = this.originalValue.score;
        }
    }

    // Given a new score, save this back into the grouped grade dict.
    saveValue(value, ctrlDown) {
        // The value to save is a 2-D array of ``[[single_value]]``, probably to make internals easier to use (see the ``_baseEditor.saveValue``, which calls ``populatefromArray``, which expects a 2-D array).
        let single_value = value[0][0];

        // Don't edit the old grade -- it needs to stay unchanged if the validator wants to revert back to it. Instead, create a new instance.
        let grouped_grade = Object.assign(
            {},
            this.hot.getDataAtCell(this.row, this.col)
        );
        grouped_grade.score = single_value;

        // Repack the grade into a 2-D array. Don't allow multiple edits by passing ``false`` for ``ctrlDown`` (ctrl+enter in Excel evidently applies the same entry to all selected cells). TODO: this could be implemented, but who would use it?
        super.saveValue([[grouped_grade]], false);
    }
}
