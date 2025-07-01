from pydantic_ai import Agent, RunContext
from schemas import InterviewTranscript, ArticleDraft, EditorFeedback, InterviewMessage
from pydantic import BaseModel
from typing import List

# Interviewer Agent
interviewer_agent = Agent(
    "openai:gpt-4-1106-preview",
    system_prompt=(
        "You are a skilled interviewer conducting an in-depth interview. "
        "Ask thoughtful, probing questions to explore the topic deeply. "
        "Generate follow-up questions based on the interviewee's responses. "
        "Maintain a professional yet conversational tone."
    ),
    deps_type=None,
    result_type=InterviewTranscript,
)

# Mock interview function for testing (before voice integration)
def mock_interview(topic: str) -> InterviewTranscript:
    """Generate a mock interview transcript for testing purposes."""
    return InterviewTranscript(messages=[
        InterviewMessage(speaker="Interviewer", content=f"Today we're discussing {topic}. Can you tell me why this topic is important in today's context?"),
        InterviewMessage(speaker="Interviewee", content="This topic is crucial because it affects how we approach modern challenges in technology and society."),
        InterviewMessage(speaker="Interviewer", content="What are the main challenges you see in this area?"),
        InterviewMessage(speaker="Interviewee", content="The biggest challenges include lack of awareness, resource constraints, and the need for better collaboration."),
        InterviewMessage(speaker="Interviewer", content="How do you think we can address these challenges effectively?"),
        InterviewMessage(speaker="Interviewee", content="We need a multi-faceted approach involving education, policy changes, and technological innovation."),
    ])

# Writer Agent with structured context handling
class WriterContext(BaseModel):
    transcript: InterviewTranscript
    target_audience: str
    version: int
    editor_feedback: List[str] = []

# Create the writer agent with a base system prompt
writer_agent = Agent(
    "openai:gpt-4-1106-preview",
    system_prompt=(
        "You are a professional writer creating articles from interview transcripts. "
        "Analyze the interview content and create a well-structured, engaging article. "
        "Tailor the tone and complexity to the target audience. "
        "Include a compelling title that captures the essence of the interview."
    ),
    deps_type=WriterContext,
    result_type=ArticleDraft,
)

# Add dynamic system prompt based on editor feedback
@writer_agent.system_prompt
def writer_dynamic_prompt(ctx: RunContext[WriterContext]) -> str:
    if ctx.deps.editor_feedback:
        feedback_text = "\n".join(f"- {critique}" for critique in ctx.deps.editor_feedback)
        return f"Editor feedback from previous version:\n{feedback_text}\n\nAddress all these points in your revision."
    return ""

# Editor Agent
class EditorContext(BaseModel):
    draft: ArticleDraft

editor_agent = Agent(
    "openai:gpt-4-1106-preview",
    system_prompt=(
        "You are a critical editor reviewing article drafts. "
        "Evaluate the article for: clarity, coherence, factual accuracy, tone consistency, "
        "engagement level, and alignment with best practices in journalism. "
        "Provide specific, actionable feedback. "
        "Only approve (is_approved=true) if the article meets professional publication standards. "
        "Be thorough but constructive in your critiques."
    ),
    deps_type=EditorContext,
    result_type=EditorFeedback,
) 