#!/usr/bin/env python3
"""
Advanced Research Execution Script for MeUnique Platform
Integrates with OpenAI API for real-time research enhancement and validation
"""

import os
import json
import asyncio
import aiohttp
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any
import openai
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ResearchConfig:
    """Configuration for research execution"""
    openai_api_key: str
    github_token: Optional[str] = None
    linkedin_api_key: Optional[str] = None
    huggingface_token: Optional[str] = None
    max_concurrent_requests: int = 5
    cost_limit_per_session: float = 50.0
    output_directory: str = "./research_output"

class MeUniqueResearchExecutor:
    """Advanced research executor with API integration"""
    
    def __init__(self, config: ResearchConfig):
        self.config = config
        self.openai_client = openai.OpenAI(api_key=config.openai_api_key)
        self.session_cost = 0.0
        self.research_results = {}
        
        # Create output directory
        os.makedirs(config.output_directory, exist_ok=True)
        
        # Research prompts optimized for comprehensive analysis
        self.research_prompts = {
            "gap_analysis": """
            You are an expert system analyst specializing in comprehensive specification analysis.
            
            TASK: Perform deep gap analysis of the MeUnique platform specification.
            
            SPECIFICATION COMPONENTS TO ANALYZE:
            {specification_content}
            
            ANALYSIS REQUIREMENTS:
            1. Identify missing functional requirements
            2. Assess technical architecture completeness
            3. Evaluate cultural intelligence framework coverage
            4. Analyze market validation thoroughness
            5. Review implementation readiness
            
            Provide comprehensive analysis in JSON format:
            {{
                "missing_components": ["component1", "component2"],
                "enhancement_opportunities": ["opportunity1", "opportunity2"],
                "technical_gaps": ["gap1", "gap2"],
                "cultural_intelligence_gaps": ["gap1", "gap2"],
                "market_validation_needs": ["need1", "need2"],
                "implementation_blockers": ["blocker1", "blocker2"],
                "priority_recommendations": ["rec1", "rec2"],
                "estimated_effort": "hours/days/weeks",
                "confidence_score": 0-100
            }}
            """,
            
            "market_intelligence": """
            You are a market intelligence expert specializing in global tech hiring trends.
            
            TASK: Conduct comprehensive market research for cultural intelligence in tech hiring.
            
            RESEARCH FOCUS:
            Target Markets: {target_markets}
            Competitive Landscape: {competitors}
            Technology Trends: {tech_trends}
            
            RESEARCH REQUIREMENTS:
            1. Market size and growth projections
            2. Competitive positioning analysis
            3. Cultural hiring trend analysis
            4. Technology adoption patterns
            5. Regulatory environment assessment
            
            Provide market intelligence in JSON format:
            {{
                "market_size": {{"total": "value", "growth_rate": "percentage"}},
                "competitive_analysis": {{"strengths": [], "weaknesses": [], "opportunities": []}},
                "cultural_trends": ["trend1", "trend2"],
                "technology_adoption": {{"emerging": [], "mature": [], "declining": []}},
                "regulatory_considerations": ["consideration1", "consideration2"],
                "market_opportunities": ["opportunity1", "opportunity2"],
                "entry_barriers": ["barrier1", "barrier2"],
                "success_factors": ["factor1", "factor2"]
            }}
            """,
            
            "technical_validation": """
            You are a senior technical architect specializing in AI-powered platforms.
            
            TASK: Validate technical architecture and implementation strategy.
            
            TECHNICAL COMPONENTS:
            Architecture: {architecture_details}
            API Integrations: {api_integrations}
            Scalability Requirements: {scalability_needs}
            
            VALIDATION REQUIREMENTS:
            1. Architecture scalability assessment
            2. API integration feasibility
            3. Performance optimization opportunities
            4. Security and compliance validation
            5. Implementation complexity analysis
            
            Provide technical validation in JSON format:
            {{
                "architecture_assessment": {{"scalability": "rating", "maintainability": "rating"}},
                "api_integration_feasibility": {{"openai": "feasible/challenging", "github": "feasible/challenging"}},
                "performance_optimization": ["optimization1", "optimization2"],
                "security_considerations": ["consideration1", "consideration2"],
                "implementation_complexity": "low/medium/high",
                "resource_requirements": {{"development": "estimate", "infrastructure": "estimate"}},
                "risk_factors": ["risk1", "risk2"],
                "mitigation_strategies": ["strategy1", "strategy2"]
            }}
            """,
            
            "cultural_intelligence_research": """
            You are a cultural

 intelligence expert with deep knowledge of global workplace cultures.
            
            TASK: Conduct comprehensive cultural intelligence research for global tech hiring.
            
            CULTURAL RESEARCH SCOPE:
            Markets: {target_markets}
            Cultural Dimensions: {cultural_dimensions}
            Hiring Practices: {hiring_practices}
            
            RESEARCH REQUIREMENTS:
            1. Cultural dimension analysis for each market
            2. Communication style patterns
            3. Professional etiquette variations
            4. Bias identification and mitigation strategies
            5. Cross-cultural team integration best practices
            
            Provide cultural intelligence research in JSON format:
            {{
                "cultural_profiles": {{
                    "market": {{
                        "communication_style": "description",
                        "hierarchy_preference": "description",
                        "decision_making": "description",
                        "feedback_culture": "description",
                        "work_life_balance": "description"
                    }}
                }},
                "bias_mitigation_strategies": ["strategy1", "strategy2"],
                "integration_best_practices": ["practice1", "practice2"],
                "cultural_adaptation_indicators": ["indicator1", "indicator2"],
                "success_metrics": ["metric1", "metric2"]
            }}
            """
        }
    
    async def execute_comprehensive_research(self, specification_files: List[str]) -> Dict[str, Any]:
        """Execute comprehensive research across all areas"""
        logger.info("Starting comprehensive research execution")
        
        # Load specification content
        specification_content = await self._load_specification_files(specification_files)
        
        # Execute research tasks in parallel
        research_tasks = [
            self._execute_gap_analysis(specification_content),
            self._execute_market_intelligence(),
            self._execute_technical_validation(specification_content),
            self._execute_cultural_intelligence_research()
        ]
        
        results = await asyncio.gather(*research_tasks, return_exceptions=True)
        
        # Compile comprehensive research report
        comprehensive_report = {
            "execution_timestamp": datetime.now().isoformat(),
            "total_cost": self.session_cost,
            "gap_analysis": results[0] if not isinstance(results[0], Exception) else {"error": str(results[0])},
            "market_intelligence": results[1] if not isinstance(results[1], Exception) else {"error": str(results[1])},
            "technical_validation": results[2] if not isinstance(results[2], Exception) else {"error": str(results[2])},
            "cultural_intelligence": results[3] if not isinstance(results[3], Exception) else {"error": str(results[3])}
        }
        
        # Save comprehensive report
        await self._save_research_report(comprehensive_report)
        
        return comprehensive_report
    
    async def _execute_gap_analysis(self, specification_content: str) -> Dict[str, Any]:
        """Execute comprehensive gap analysis"""
        logger.info("Executing gap analysis")
        
        prompt = self.research_prompts["gap_analysis"].format(
            specification_content=specification_content[:8000]  # Limit content size
        )
        
        try:
            response = await self._call_openai_api(
                prompt=prompt,
                model="gpt-4",
                max_tokens=2000,
                temperature=0.3
            )
            
            return json.loads(response)
        except Exception as e:
            logger.error(f"Gap analysis failed: {e}")
            return {"error": str(e)}
    
    async def _execute_market_intelligence(self) -> Dict[str, Any]:
        """Execute market intelligence research"""
        logger.info("Executing market intelligence research")
        
        market_data = {
            "target_markets": ["US", "Israel", "Germany", "France", "UK"],
            "competitors": ["LinkedIn Talent", "Greenhouse", "HireVue", "Pymetrics"],
            "tech_trends": ["AI hiring", "Remote work", "Cultural diversity", "Skills-based hiring"]
        }
        
        prompt = self.research_prompts["market_intelligence"].format(**market_data)
        
        try:
            response = await self._call_openai_api(
                prompt=prompt,
                model="gpt-4",
                max_tokens=2500,
                temperature=0.4
            )
            
            return json.loads(response)
        except Exception as e:
            logger.error(f"Market intelligence failed: {e}")
            return {"error": str(e)}
    
    async def _execute_technical_validation(self, specification_content: str) -> Dict[str, Any]:
        """Execute technical architecture validation"""
        logger.info("Executing technical validation")
        
        technical_data = {
            "architecture_details": "Microservices with React frontend, Node.js backend, PostgreSQL database",
            "api_integrations": "OpenAI, HuggingFace, GitHub, LinkedIn APIs",
            "scalability_needs": "Global deployment, high availability, auto-scaling"
        }
        
        prompt = self.research_prompts["technical_validation"].format(**technical_data)
        
        try:
            response = await self._call_openai_api(
                prompt=prompt,
                model="gpt-4-turbo",
                max_tokens=2000,
                temperature=0.2
            )
            
            return json.loads(response)
        except Exception as e:
            logger.error(f"Technical validation failed: {e}")
            return {"error": str(e)}
    
    async def _execute_cultural_intelligence_research(self) -> Dict[str, Any]:
        """Execute cultural intelligence research"""
        logger.info("Executing cultural intelligence research")
        
        cultural_data = {
            "target_markets": ["United States", "Israel", "Germany", "France", "United Kingdom"],
            "cultural_dimensions": ["Communication style", "Hierarchy", "Innovation", "Risk tolerance"],
            "hiring_practices": ["Interview styles", "Decision making", "Onboarding", "Performance evaluation"]
        }
        
        prompt = self.research_prompts["cultural_intelligence_research"].format(**cultural_data)
        
        try:
            response = await self._call_openai_api(
                prompt=prompt,
                model="gpt-4",
                max_tokens=3000,
                temperature=0.3
            )
            
            return json.loads(response)
        except Exception as e:
            logger.error(f"Cultural intelligence research failed: {e}")
            return {"error": str(e)}
    
    async def _call_openai_api(self, prompt: str, model: str, max_tokens: int, temperature: float) -> str:
        """Call OpenAI API with cost tracking"""
        if self.session_cost >= self.config.cost_limit_per_session:
            raise Exception(f"Cost limit exceeded: ${self.session_cost:.2f}")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert research analyst. Provide comprehensive, accurate analysis in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Estimate cost (approximate)
            estimated_cost = self._estimate_api_cost(model, len(prompt), max_tokens)
            self.session_cost += estimated_cost
            
            logger.info(f"API call completed. Estimated cost: ${estimated_cost:.3f}, Total: ${self.session_cost:.2f}")
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise
    
    def _estimate_api_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Estimate API cost based on model and token usage"""
        costs = {
            "gpt-4": {"input": 0.03/1000, "output": 0.06/1000},
            "gpt-4-turbo": {"input": 0.01/1000, "output": 0.03/1000},
            "gpt-3.5-turbo": {"input": 0.001/1000, "output": 0.002/1000}
        }
        
        model_cost = costs.get(model, costs["gpt-4"])
        return (input_tokens * model_cost["input"]) + (output_tokens * model_cost["output"])
    
    async def _load_specification_files(self, file_paths: List[str]) -> str:
        """Load and combine specification files"""
        combined_content = ""
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    combined_content += f"\n\n=== {file_path} ===\n{content}"
            except Exception as e:
                logger.warning(f"Could not load file {file_path}: {e}")
        
        return combined_content
    
    async def _save_research_report(self, report: Dict[str, Any]) -> None:
        """Save comprehensive research report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.config.output_directory, f"research_report_{timestamp}.json")
        
        try:
            with open(report_path, 'w', encoding='utf-8') as file:
                json.dump(report, file, indent=2, ensure_ascii=False)
            
            logger.info(f"Research report saved to: {report_path}")
        except Exception as e:
            logger.error(f"Failed to save research report: {e}")
    
    async def analyze_csv_candidates(self, csv_path: str) -> Dict[str, Any]:
        """Analyze candidates from CSV file using AI"""
        logger.info(f"Analyzing candidates from CSV: {csv_path}")
        
        try:
            df = pd.read_csv(csv_path)
            candidates = df.to_dict('records')
            
            analysis_results = []
            
            for candidate in candidates[:10]:  # Limit to first 10 for cost control
                try:
                    cultural_analysis = await self._analyze_candidate_cultural_fit(candidate)
                    technical_analysis = await self._analyze_candidate_technical_skills(candidate)
                    
                    analysis_results.append({
                        "candidate_id": candidate.get("id", "unknown"),
                        "name": candidate.get("name", "unknown"),
                        "cultural_analysis": cultural_analysis,
                        "technical_analysis": technical_analysis,
                        "overall_score": self._calculate_overall_score(cultural_analysis, technical_analysis)
                    })
                    
                    # Add delay to respect rate limits
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Failed to analyze candidate: {e}")
                    analysis_results.append({
                        "candidate_id": candidate.get("id", "unknown"),
                        "error": str(e)
                    })
            
            # Save candidate analysis results
            await self._save_candidate_analysis(analysis_results)
            
            return {
                "total_candidates": len(candidates),
                "analyzed_candidates": len(analysis_results),
                "analysis_results": analysis_results,
                "total_cost": self.session_cost
            }
            
        except Exception as e:
            logger.error(f"CSV analysis failed: {e}")
            return {"error": str(e)}
    
    async def _analyze_candidate_cultural_fit(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze individual candidate cultural fit"""
        prompt = f"""
        Analyze the cultural fit of this candidate for global tech hiring:
        
        Candidate Profile: {json.dumps(candidate)}
        
        Provide analysis in JSON format:
        {{
            "cultural_score": 0-100,
            "communication_style": "direct/diplomatic/balanced",
            "adaptation_potential": "high/medium/low",
            "market_preferences": ["market1", "market2"],
            "strengths": ["strength1", "strength2"],
            "development_areas": ["area1", "area2"]
        }}
        """
        
        try:
            response = await self._call_openai_api(
                prompt=prompt,
                model="gpt-4",
                max_tokens=800,
                temperature=0.3
            )
            return json.loads(response)
        except Exception as e:
            return {"error": str(e), "cultural_score": 0}
    
    async def _analyze_candidate_technical_skills(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze individual candidate technical skills"""
        prompt = f"""
        Analyze the technical skills of this candidate:
        
        Candidate Profile: {json.dumps(candidate)}
        
        Provide analysis in JSON format:
        {{
            "technical_score": 0-100,
            "skill_proficiency": {{"skill": "level"}},
            "experience_level": "junior/mid/senior",
            "learning_potential": "high/medium/low",
            "technical_strengths": ["strength1", "strength2"],
            "skill_gaps": ["gap1", "gap2"]
        }}
        """
        
        try:
            response = await self._call_openai_api(
                prompt=prompt,
                model="gpt-4",
                max_tokens=800,
                temperature=0.3
            )
            return json.loads(response)
        except Exception as e:
            return {"error": str(e), "technical_score": 0}
    
    def _calculate_overall_score(self, cultural: Dict[str, Any], technical: Dict[str, Any]) -> int:
        """Calculate overall candidate score"""
        cultural_score = cultural.get("cultural_score", 0)
        technical_score = technical.get("technical_score", 0)
        
        # Weighted average: 60% technical, 40% cultural
        overall_score = (technical_score * 0.6) + (cultural_score * 0.4)
        return round(overall_score)
    
    async def _save_candidate_analysis(self, analysis_results: List[Dict[str, Any]]) -> None:
        """Save candidate analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_path = os.path.join(self.config.output_directory, f"candidate_analysis_{timestamp}.json")
        
        try:
            with open(analysis_path, 'w', encoding='utf-8') as file:
                json.dump(analysis_results, file, indent=2, ensure_ascii=False)
            
            logger.info(f"Candidate analysis saved to: {analysis_path}")
        except Exception as e:
            logger.error(f"Failed to save candidate analysis: {e}")

# Example usage and configuration
async def main():
    """Main execution function"""
    # Configuration
    config = ResearchConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
        github_token=os.getenv("GITHUB_TOKEN"),
        linkedin_api_key=os.getenv("LINKEDIN_API_KEY"),
        huggingface_token=os.getenv("HUGGINGFACE_TOKEN"),
        max_concurrent_requests=3,
        cost_limit_per_session=25.0,
        output_directory="./research_output"
    )
    
    # Initialize research executor
    executor = MeUniqueResearchExecutor(config)
    
    # Specification files to analyze
    specification_files = [
        "COMPLETE_VERIFIED_SPECIFICATION.md",
        "MASTER_RESEARCH_PROMPTS.md",
        "EXTERNAL_RESEARCH_ENHANCEMENT_FRAMEWORK.md"
    ]
    
    try:
        # Execute comprehensive research
        logger.info("Starting comprehensive research execution")
        research_results = await executor.execute_comprehensive_research(specification_files)
        
        print("\n" + "="*50)
        print("COMPREHENSIVE RESEARCH COMPLETED")
        print("="*50)
        print(f"Total Cost: ${research_results.get('total_cost', 0):.2f}")
        print(f"Execution Time: {research_results.get('execution_timestamp')}")
        
        # Display key findings
        if "gap_analysis" in research_results and not research_results["gap_analysis"].get("error"):
            gap_analysis = research_results["gap_analysis"]
            print(f"\nGap Analysis - Confidence: {gap_analysis.get('confidence_score', 0)}%")
            print(f"Missing Components: {len(gap_analysis.get('missing_components', []))}")
            print(f"Enhancement Opportunities: {len(gap_analysis.get('enhancement_opportunities', []))}")
        
        if "market_intelligence" in research_results and not research_results["market_intelligence"].get("error"):
            market_intel = research_results["market_intelligence"]
            print(f"\nMarket Intelligence:")
            print(f"Market Opportunities: {len(market_intel.get('market_opportunities', []))}")
            print(f"Success Factors: {len(market_intel.get('success_factors', []))}")
        
        # Example CSV analysis (if CSV file exists)
        csv_path = "sample_candidates.csv"
        if os.path.exists(csv_path):
            logger.info("Analyzing sample candidates from CSV")
            candidate_results = await executor.analyze_csv_candidates(csv_path)
            print(f"\nCandidate Analysis:")
            print(f"Total Candidates: {candidate_results.get('total_candidates', 0)}")
            print(f"Analyzed: {candidate_results.get('analyzed_candidates', 0)}")
        
    except Exception as e:
        logger.error(f"Research execution failed: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
