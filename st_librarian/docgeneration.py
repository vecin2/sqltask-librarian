import shutil
from pathlib import Path

from mdutils.mdutils import MdUtils

from st_librarian.document import EntitySection, TemplateSection
from st_librarian.sqltasklib import ViewType


class DocGenerator(object):
    def __init__(self, tasklib):
        self.tasklib = tasklib

    def generate(
        self, path=Path("docs/templates.md"), view_type=ViewType.BY_FOLDER
    ):
        mdFile = MdUtils(file_name=path.name, title="SQLTask Library")
        sections = self._sections(view_type)
        self.append_summary(mdFile, sections)
        contents_marker = self.append_table_of_contents(mdFile)
        for section in sections:
            print(f"Generating Section {section.title}")
            section.append_to(mdFile)
        mdFile.new_table_of_contents(
            table_title="Tables of Contents", depth=2, marker=contents_marker
        )

        mdFile.create_md_file()
        shutil.move(src=path.name, dst=str(path))

        print(f"\n{path} has been generated")

    def append_table_of_contents(self, mdFile):
        return mdFile.create_marker("tableOfContents")

    def append_summary(self, mdFile, sections):
        counter = 0
        summary = ""
        for section in sections:
            if summary:
                summary += ", "
            summary += f"{len(section.templates)} {section.anchor()}"
            counter += len(section.templates)
        summary = f"This  library has currently a total of {counter} templates, divided in {len(sections)} sections; {summary}\n"
        mdFile.new_paragraph(summary)

    def _sections(self, view_type):
        result = []
        sections = self._template_sections(view_type)
        for section_name, templates in sections.items():
            result.append(self._make_section(section_name, templates))
        return result

    def _template_sections(self, view_type):
        return self.tasklib.sections(view_type)

    def _make_section(self, name, templates):
        md_section = EntitySection(name)
        for template in templates:
            md_section.append(TemplateSection(template))
        return md_section
