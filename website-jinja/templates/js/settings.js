/**
 * Created by Angelica Yunshu Li on 8/2/2016.
 */
if (!String.prototype.format) {
    String.prototype.format = function () {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}


$(document).ready(function () {

    /* add url row */
    $("section").on("click", "td.add", function () {
        var row = $(this).parent();
        var last_btn = $(row).prev().children(":last").children();
        if (last_btn.length > 0) {
            var last_btn_number = last_btn.attr("name").slice(7).split("-");
            var new_btn_number = last_btn_number[0] + "-" + (last_btn_number[1] + 1);
        } else {
            var course_number = $(row).parent().parent().prev().children(":last").attr("name").slice(6);
            var new_btn_number = course_number + "-" + 0;
        }
        var new_row = "<tr> \
                    <td class='delete btn' align='right'><img src='/images/delete.png' class='icon'/></td>\
                    <td class='title'><input name='btn{0}'></td>\
                    <td align='left' class='url'><input class='url' name='btn_url{0}' text='{{courseinfo.get(course).get(name)}}'/></td>\
                    </tr>".format(new_btn_number);
        $(row).before(new_row);
        var col = $(row).prev().children()[1];
        var focusbox = $(col).children("input");
        console.log(focusbox);
        focusbox.focus();
    });

    /* detele url row */
    $("section").on("click", "td.delete", function () {
        var row = $(this).parent();
        $(row).fadeOut().remove();
    });
    $("section").on("mouseenter", "td.delete", function () {
        $(this).find("img").remove();
        $(this).prepend("<span>Delete</span>");
    });
    $("section").on("mouseleave", "td.delete", function () {
        $(this).find("span").remove();
        $(this).append("<img src='/images/delete.png' class='icon'/>");
    });

    /*TODO: edit courseid*/
    $("section").on("click", "img.edit", function () {
        var input = $(this).parent().next();
        var input_value = $(input).attr("value");
        var input_name = $(input).attr("name");
        var h2 = $(input).parent();
        // $(h2).contents().filter(function(){              //to remove text only
        //     return this.nodeType === 3;
        // }).remove();
        $(h2).next().prepend('<tr> \
                        <td></td> \
                        <td class="title">Course ID</td> \
                        <td align="left" class="url"><input name="{0}" value="{1}"></td> \
                    </tr>'.format(input_name, input_value));
        $(h2).remove();


    });

    /*delete course*/
    $("section").on("click", "img.delete", function () {
        var div = $(this).parent().parent().parent();
        $(div).fadeOut().remove();
    });


    /* add course*/
    // add new course function
    var new_course_id = document.getElementsByTagName("table").length;
    var default_info_list = ['Course Website', 'Homework', 'Calendar', 'Syllabus', 'Grades'];

    function new_course() {
        var new_course = '<table class="clear" align="center"> \
            <tr> \
                <td><input type="hidden" name="new" value="{0}"></td> \
                <td class="title">Course ID</td> \
                <td align="left" class="url"><input class="new-course" name="course{0}" placeholder="e.g. CS125"></td> \
            </tr>'.format(new_course_id);
        for (i = 0; i < default_info_list.length; i++) {
            var title = default_info_list[i];
            new_course += '<tr> \
                                <input type="hidden" name="bid{1}-{2}" value="{2}">\
                                <td class="delete btn" align="right"><img src="/images/delete.png" class="icon"/></td> \
                                <td class="title">{0}<input type="hidden" name="btn{1}-{2}" value="{0}"></td> \
                                <td align="left" class="url"><input name="btn_url{1}-{2}" class="url" placeholder="{0} URL" /></td> \
                            </tr>'.format(default_info_list[i], new_course_id, i);
        }
        ;
        new_course += '<tr> \
                        <td class="add btn" align="right"><img src="/images/add.png" class="icon"/></td> \
                        </tr>';
        new_course_id += 1;
        return new_course;
    };

    $("#add-course").click(function () {
        $(this).after(new_course());
        var focusbox = document.getElementsByClassName("new-course")[0];
        focusbox.focus();

    })

    /* image upload */
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#schedule').attr('src', e.target.result);
                $('#schedule').show();
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#imgInp").change(function () {
        readURL(this);
    });


});