from typing import Literal

from loguru import logger

from .ai_api import request_model

RewriteStyle = Literal["professional", "concise", "impactful", "quantitative"]


def rewrite_achievement_statement(
    achievement_text: str,
    style: RewriteStyle = "professional",
    context: str = ""
) -> str:
    """
    Rewrite and enhance an achievement statement to make it more impactful.

    Args:
        achievement_text: The original achievement statement to rewrite
        style: The style of rewriting (professional, concise, impactful, quantitative)
        context: Optional additional context about the achievement

    Returns:
        Enhanced achievement statement
    """

    if not achievement_text.strip():
        return "Please provide an achievement statement to rewrite."

    prompt = f"""
    Please rewrite the following achievement statement to make it more impactful and professional.
    Focus on making it {style} in style.

    **Original Achievement Statement:**
    "{achievement_text}"

    **Additional Context (if provided):**
    {context if context else "No additional context provided."}

    **Task:**
    Rewrite the achievement statement following these guidelines:

    1. **Make it quantifiable**: If possible, include specific numbers, percentages, or metrics to demonstrate impact.
    2. **Use strong action verbs**: Start with powerful verbs like "Led", "Implemented", "Achieved", "Optimized", etc.
    3. **Focus on results**: Emphasize outcomes and benefits rather than just activities.
    4. **Be concise yet comprehensive**: Keep it impactful but not verbose.
    5. **Maintain truthfulness**: Do not add information that isn't implied in the original statement.

    **Style-specific instructions:**
    - **professional**: Formal, business-appropriate language suitable for resumes/CVs
    - **concise**: Short and to the point while maintaining impact
    - **impactful**: Emphasize the significance and scale of the achievement
    - **quantitative**: Focus heavily on metrics and measurable outcomes

    **Important:**
    - The output should be ONLY the rewritten achievement statement.
    - No extra explanations, introductions, or formatting.
    - Keep it as a single, well-crafted sentence or short paragraph.
    - Ensure it's ready to use in a resume or professional context.
    """

    response = request_model(prompt)
    if response is None:
        # Provide a fallback if AI fails
        logger.warning("AI service unavailable, using basic enhancement")
        # Simple enhancement: capitalize first letter and add period if needed
        enhanced = achievement_text.strip()
        if not enhanced.endswith('.'):
            enhanced += '.'
        return enhanced[0].upper() + enhanced[1:] if enhanced else achievement_text

    # Clean up the response - remove any extra whitespace or quotes
    rewritten = response.strip()
    if rewritten.startswith('"') and rewritten.endswith('"'):
        rewritten = rewritten[1:-1]
    if rewritten.startswith("'") and rewritten.endswith("'"):
        rewritten = rewritten[1:-1]

    return rewritten
