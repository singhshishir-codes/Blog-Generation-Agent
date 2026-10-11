

from src.states.blogstate import BlogState


class BlogNode:
    """
    A class to represent the blog node
    """
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state:BlogState):
        """
        Create a title for blog
        """
        if "topic" in state and state["topic"]:
            prompt = """
                    You are an expert bolg content writer, use markdown formating, generate blog title for the {topic}.
                    This topic should be creative and SEO friendly
                    """

            system_message = prompt.format(topic = state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": response.content}}


    def content_generation(self, state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic = state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}



    def translation(self, state: BlogState):
        if "blog" not in state or not state["blog"]:
            return {}

        blog_title = state["blog"].get("title", "")
        blog_content = state["blog"].get("content", "")

        if isinstance(blog_content, dict):
            blog_content = blog_content.get("content", "")

        title_prompt = """
        Translate this blog title into {current_language}.
        - Maintain the original tone, style and formatting.
        - Return only the translated title.

        {blog_title}
        """

        content_prompt = """
        Translate the following blog content into {current_language}.
        - Maintain the original tone, style and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.
        - Return only the translated content, preserving its Markdown formatting.

        {blog_content}
        """

        translated_title = self.llm.invoke(
            title_prompt.format(
                current_language=state["current_language"],
                blog_title=blog_title,
            )
        )
        translated_content = self.llm.invoke(
            content_prompt.format(
                current_language=state["current_language"],
                blog_content=blog_content,
            )
        )

        return {
            "blog": {
                "title": translated_title.content,
                "content": translated_content.content,
            }
        }

    def route(self, state:BlogState):
        return {"current_language": state["current_language"]}

    def route_decision(self, state:BlogState):
        """
        Route content to the respective translation function.
        """
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french":
            return "french"
        else:
            return state["current_language"]



        