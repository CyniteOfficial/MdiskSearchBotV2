from telegraph.aio import Telegraph
import markdown


async def telegraph_handler(title, html, author):
    telegraph = Telegraph()
    if len(title) >= 20:
        title = title[:20]
    await telegraph.create_account(short_name=title, author_name=author)
    response = await telegraph.create_page(
        title=title,
        html_content=html,
        author_name=author
    )
    return response['url']


async def markdown_to_html(markdown_txt):
    md = markdown.Markdown()
    html = md.convert(markdown_txt)
    return html

