from pathlib import Path

from mdutils.tools.Header import Header


class StringBuilder(object):
    def __init__(self):
        self.segments = []

    def append(self, text):
        self.segments.append(text)
        return self

    def append_line(self, text):
        if self.segments:
            self.append("\\").append("\n")
        self.append(text)

    def build(self):
        return "".join(self.segments)


class MarkdownRelativeLink(object):
    def __init__(self, name, url_to):
        self.name = name
        self.url_to = url_to

    def render(self, save_location):
        return f"[{self.name}]({self._get_url(save_location)})"

    def _get_url(self, save_location):
        result = ""

        for parent in save_location.parents:
            result = ".." / parent
        return result / self.url_to


class InlineImage(MarkdownRelativeLink):
    def render(self, save_location):
        return "!" + super().render(save_location)

    def append_to(self, mdFile):
        mdFile.new_line(
            mdFile.new_inline_image(
                text=self.name, path=str(self._get_url(Path(mdFile.file_name)))
            )
        )
        mdFile.new_line("Image: " + self.name, bold_italics_code="b")
        mdFile.new_line("")


class EntitySection(object):
    def __init__(self, title):
        self.templates = []
        self.title = title
        self.sb = StringBuilder()

    def anchor(self):
        return Header.header_anchor(self.title)

    def append_to(self, mdFile):
        mdFile.new_header(level=1, title=self.title)
        summary = (
            f"Currently, there are {len(self.templates)} templates in this section"
        )
        mdFile.new_line(summary)
        for template in self.templates:
            template.append_to(mdFile)

    def append(self, template):
        self.templates.append(template)


class TemplateSection(object):
    def __init__(self, template):
        self.template = template

    @property
    def template_link(self):
        return MarkdownRelativeLink(self.template.filename(), self.template.relpath())

    @property
    def test_link(self):
        testpath = self.template.testpath()
        return MarkdownRelativeLink(testpath.name, testpath)

    def images(self):
        result = []
        for image in self.template.images():
            image_name = image.stem.replace(self.template.name(), "")
            result.append(
                InlineImage(
                    image_name, image.relative_to(self.template.library_root.parent)
                )
            )
        return result

    def append_to(self, mdFile):
        mdFile.new_header(level=2, title=self.template.display_name())
        self.append_related_content(mdFile)
        mdFile.new_paragraph(self.template.oneline_description())
        mdFile.new_paragraph(self.template.long_description())
        for image in self.images():
            image.append_to(mdFile)
            # mdFile.new_paragraph(image.render(Path(mdFile.file_name)))

    def append_related_content(self, mdFile):
        mdFile.new_line(
            "*Template:* " + self.template_link.render(Path(mdFile.file_name))
        )
        mdFile.new_line("*Test:* " + self.test_link.render(Path(mdFile.file_name)))
        self.append_anchors(mdFile, "Tasks", self.template.related_tasks())
        self.append_anchors(mdFile, "Views", self.template.related_views())

    def append_anchors(self, mdFile, content_name, templates):
        anchors = []
        for task in templates:
            anchors.append(mdFile.header.header_anchor(task.display_name()))

        if anchors:
            mdFile.new_line(f"*{content_name}:* " + ", ".join(anchors))
