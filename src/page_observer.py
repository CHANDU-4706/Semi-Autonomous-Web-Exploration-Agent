
class PageObserver:
    def __init__(self, page):
        self.page = page

    def observe(self):
        """Scans the page and returns a structured observation."""
        if not self.page:
            return {}

        # Basic Info
        url = self.page.url
        title = self.page.title()
        
        # Interactive Elements
        # Get visible buttons and links
        buttons = self.page.eval_on_selector_all("button, input[type='submit'], a.btn", 
            """elements => elements.map(e => ({
                text: e.innerText.trim(), 
                id: e.id, 
                name: e.name, 
                tag: e.tagName,
                visible: e.offsetParent !== null
            })).filter(e => e.visible && e.text.length > 0)
            """)
        
        # Inputs
        inputs = self.page.eval_on_selector_all("input:not([type='submit']):not([type='hidden']), textarea", 
            """elements => elements.map(e => ({
                id: e.id, 
                name: e.name, 
                placeholder: e.placeholder,
                type: e.type,
                visible: e.offsetParent !== null
            })).filter(e => e.visible)
            """)

        # Links (Filtering for relevant navigation links if possible, or just first few)
        links = self.page.eval_on_selector_all("a[href]", 
            """elements => elements.slice(0, 20).map(e => ({
                text: e.innerText.trim(), 
                href: e.href,
                visible: e.offsetParent !== null
            })).filter(e => e.visible && e.text.length > 0)
            """)

        # content summary (simplistic)
        body_text = self.page.inner_text("body")
        summary = body_text[:500].replace("\n", " ") + "..."

        # Error detection (Basic heuristics)
        errors = []
        if "error" in body_text.lower():
            # Try to frame it
            pass 

        observation = {
            "url": url,
            "title": title,
            "buttons": buttons,
            "inputs": inputs,
            "links": links,
            "page_text_summary": summary,
            "errors": errors
        }
        return observation
