/**
 * Created by Angelica Yunshu Li on 8/2/2016.
 */
if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}








$(document).ready(function(){


    /* add url row */
    var new_row = "<tr> \
                    <td class='delete btn' align='right'><img src='/images/delete.png' class='icon'/></td>\
                    <td class='title'><input name='new-btn'></td>\
                    <td align='left' class='url'><input class='url' name='new-btn-url' text='{{courseinfo.get(course).get(name)}}'/></td>\
                    </tr>";
    $("section").on("click","td.add",function(){
        var row = $(this).parent();
        $(row).before(new_row);
    });

    /* detele url row */
    $("section").on("click","td.delete",function(){
        var row = $(this).parent();
        $(row).fadeOut().remove();
    });
    $("section").on("mouseenter","td.delete",function(){
        $(this).find("img").remove();
       $(this).prepend("<span>Delete</span>");
    });
    $("section").on("mouseleave","td.delete",function(){
        $(this).find("span").remove();
        $(this).append("<img src='/images/delete.png' class='icon'/>");
    });

    /*TODO: edit courseid*/
    $("section").on("click","img.edit",function(){
        var courseid = $(this).text();
        var h2 = $(this).parent().parent();
        // $(h2).contents().filter(function(){              //to remove text only
        //     return this.nodeType === 3;
        // }).remove();
        $(h2).before();//TODO: add input box
        $(h2).remove();



    });

    /*delete course*/
    $("section").on("click","img.delete",function(){
        var div = $(this).parent().parent().parent();
        $(div).fadeOut().remove();
    });


    /* add course*/
    // add new course function
    if(document.getElementsByName("course0")){
        var new_course_id = 1;
    }else{
        var new_course_id = 0;
    }
    var default_info_list = ['Course Website','Homework','Calendar','Syllabus'];
    function new_course() {
        var new_course = '<table class="clear" align="center"> \
            <tr> \
                <td><input type="hidden" name="new" value="{{}}"></td> \
                <td class="title">Course ID</td> \
                <td align="left" class="url"><input name="course1" placeholder="e.g. CS125"></td> \
            </tr>'.format(new_course_id);
        for(i=0; i<default_info_list.length;i++) {
            var title = default_info_list[i];
            new_course += '<tr> \
                                <input type="hidden" name="bid{1}-{2}" value="{2}">\
                                <td class="delete btn" align="right"><img src="/images/delete.png" class="icon"/></td> \
                                <td class="title">{0}<input type="hidden" name="btn{1}-{2}" value="{0}"></td> \
                                <td align="left" class="url"><input name="btn_url{1}-{2}" class="url" placeholder="{0} URL" /></td> \
                            </tr>'.format(default_info_list[i],new_course_id,i);
        };
        new_course += '<tr> \
                        <td class="add btn" align="right"><img src="/images/add.png" class="icon"/></td> \
                        </tr>';
        new_course_id+=1;
        return new_course;
    };

    $("#add-course").click(function(){
        $(this).after(new_course());
    })


});