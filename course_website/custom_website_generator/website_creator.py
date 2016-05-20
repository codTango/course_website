def create_new_website(courses,name,semester):
    """
    Args:
        courses: a list of Course object.
    """

    #replace the course tiles placeholder generated content
    output_file = open("Angelica's_website.html",'w')
    rendered_content = main_page_content.format(course_tiles=create_course_tiles_content(courses))

    # write contents into the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
