import pytest
from unittest.mock import patch

from features.achievement_rewriter import rewrite_achievement_statement


class TestRewriteAchievementStatement:
    def test_empty_achievement_returns_message(self):
        """Test that empty achievement returns appropriate message"""
        result = rewrite_achievement_statement("")
        assert result == "Please provide an achievement statement to rewrite."

    def test_basic_enhancement_when_ai_fails(self):
        """Test basic enhancement fallback when AI service fails"""
        with patch('features.achievement_rewriter.request_model', return_value=None):
            result = rewrite_achievement_statement("i helped the team")
            assert result == "I helped the team."

    def test_ai_response_processing(self):
        """Test that AI response is properly processed"""
        mock_response = '"Enhanced team productivity by implementing streamlined workflows."'
        with patch('features.achievement_rewriter.request_model', return_value=mock_response):
            result = rewrite_achievement_statement("I helped the team")
            assert result == "Enhanced team productivity by implementing streamlined workflows."

    def test_ai_response_without_quotes(self):
        """Test AI response without surrounding quotes"""
        mock_response = "Enhanced team productivity by implementing streamlined workflows."
        with patch('features.achievement_rewriter.request_model', return_value=mock_response):
            result = rewrite_achievement_statement("I helped the team")
            assert result == "Enhanced team productivity by implementing streamlined workflows."

    @pytest.mark.parametrize("style", ["professional", "concise", "impactful", "quantitative"])
    def test_different_styles(self, style):
        """Test that different styles are passed to the prompt"""
        with patch('features.achievement_rewriter.request_model') as mock_request:
            mock_request.return_value = "Rewritten achievement"
            result = rewrite_achievement_statement("I did something", style=style)
            # Verify the function was called with the correct style in the prompt
            call_args = mock_request.call_args[0][0]
            assert style in call_args
            assert result == "Rewritten achievement"

    def test_context_included_in_prompt(self):
        """Test that context is included in the prompt"""
        with patch('features.achievement_rewriter.request_model') as mock_request:
            mock_request.return_value = "Rewritten achievement"
            result = rewrite_achievement_statement("I did something", context="In my role as manager")
            call_args = mock_request.call_args[0][0]
            assert "In my role as manager" in call_args
            assert result == "Rewritten achievement"
