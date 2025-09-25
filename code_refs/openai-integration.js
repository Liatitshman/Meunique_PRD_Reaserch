// Advanced OpenAI Integration Service for MeUnique Platform
// This service provides real API integration with your OpenAI key

import OpenAI from 'openai';

class MeUniqueOpenAIService {
  constructor(apiKey) {
    this.client = new OpenAI({
      apiKey: apiKey,
      dangerouslyAllowBrowser: true // Note: In production, use server-side proxy
    });
    
    this.culturalPrompts = {
      assessment: `You are an expert cultural intelligence analyst specializing in global tech hiring. 
      Analyze the following candidate profile for cultural fit in the specified market.
      
      Candidate Data: {candidateData}
      Target Market: {targetMarket}
      Company Stage: {companyStage}
      
      Provide analysis in the following JSON format:
      {
        "cultural_score": 0-100,
        "communication_style": "direct/diplomatic/balanced",
        "adaptation_potential": "high/medium/low",
        "key_strengths": ["strength1", "strength2"],
        "potential_challenges": ["challenge1", "challenge2"],
        "integration_recommendations": ["rec1", "rec2"],
        "confidence_level": 0-100
      }`,
      
      technical: `You are a senior technical assessor with expertise in evaluating software engineering candidates.
      Analyze the following technical profile and provide comprehensive assessment.
      
      GitHub Data: {githubData}
      LinkedIn Profile: {linkedinData}
      Target Role: {targetRole}
      
      Provide analysis in JSON format:
      {
        "technical_score": 0-100,
        "skill_proficiency": {"skill": "level"},
        "code_quality_indicators": ["indicator1", "indicator2"],
        "collaboration_patterns": "excellent/good/average/poor",
        "learning_agility": "high/medium/low",
        "technical_leadership": "strong/moderate/developing",
        "confidence_level": 0-100
      }`,
      
      risk_assessment: `You are a risk assessment specialist for technical hiring.
      Evaluate potential risks and provide mitigation strategies.
      
      Candidate Profile: {candidateProfile}
      Assessment Results: {assessmentResults}
      Target Context: {targetContext}
      
      Provide risk analysis in JSON format:
      {
        "overall_risk": "low/medium/high",
        "technical_risk": "low/medium/high",
        "cultural_risk": "low/medium/high",
        "retention_risk": "low/medium/high",
        "risk_factors": ["factor1", "factor2"],
        "mitigation_strategies": ["strategy1", "strategy2"],
        "monitoring_recommendations": ["rec1", "rec2"]
      }`
    };
    
    this.marketProfiles = {
      us: {
        name: 'United States',
        cultural_dimensions: {
          directness: 65,
          innovation: 85,
          risk_tolerance: 75,
          hierarchy: 40
        },
        communication_style: 'Results-oriented, direct but diplomatic',
        work_culture: 'Merit-based, flexible, productivity-focused'
      },
      il: {
        name: 'Israel',
        cultural_dimensions: {
          directness: 85,
          innovation: 90,
          risk_tolerance: 80,
          hierarchy: 20
        },
        communication_style: 'Very direct, informal, collaborative',
        work_culture: 'Flat hierarchy, high innovation, military leadership'
      },
      de: {
        name: 'Germany',
        cultural_dimensions: {
          directness: 85,
          innovation: 70,
          risk_tolerance: 40,
          hierarchy: 60
        },
        communication_style: 'Formal, structured, expertise-based',
        work_culture: 'Process-oriented, quality-focused, engineering excellence'
      }
    };
  }

  async analyzeCulturalFit(candidateData, targetMarket, companyStage) {
    try {
      const prompt = this.culturalPrompts.assessment
        .replace('{candidateData}', JSON.stringify(candidateData))
        .replace('{targetMarket}', this.marketProfiles[targetMarket]?.name || targetMarket)
        .replace('{companyStage}', companyStage);

      const response = await this.client.chat.completions.create({
        model: 'gpt-4',
        messages: [
          {
            role: 'system',
            content: 'You are an expert cultural intelligence analyst. Provide accurate, unbiased assessments in valid JSON format.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.3,
        max_tokens: 1500
      });

      const analysis = JSON.parse(response.choices[0].message.content);
      
      // Add market context
      analysis.market_context = this.marketProfiles[targetMarket];
      analysis.timestamp = new Date().toISOString();
      analysis.model_used = 'gpt-4';
      
      return analysis;
    } catch (error) {
      console.error('Cultural analysis error:', error);
      return {
        error: 'Analysis failed',
        message: error.message,
        cultural_score: 0,
        confidence_level: 0
      };
    }
  }

  async analyzeTechnicalProfile(githubData, linkedinData, targetRole) {
    try {
      const prompt = this.culturalPrompts.technical
        .replace('{githubData}', JSON.stringify(githubData))
        .replace('{linkedinData}', JSON.stringify(linkedinData))
        .replace('{targetRole}', targetRole);

      const response = await this.client.chat.completions.create({
        model: 'gpt-4-turbo',
        messages: [
          {
            role: 'system',
            content: 'You are a senior technical assessor. Provide comprehensive technical evaluations in valid JSON format.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.2,
        max_tokens: 2000
      });

      const analysis = JSON.parse(response.choices[0].message.content);
      analysis.timestamp = new Date().toISOString();
      analysis.model_used = 'gpt-4-turbo';
      
      return analysis;
    } catch (error) {
      console.error('Technical analysis error:', error);
      return {
        error: 'Technical analysis failed',
        message: error.message,
        technical_score: 0,
        confidence_level: 0
      };
    }
  }

  async assessRisk(candidateProfile, assessmentResults, targetContext) {
    try {
      const prompt = this.culturalPrompts.risk_assessment
        .replace('{candidateProfile}', JSON.stringify(candidateProfile))
        .replace('{assessmentResults}', JSON.stringify(assessmentResults))
        .replace('{targetContext}', JSON.stringify(targetContext));

      const response = await this.client.chat.completions.create({
        model: 'gpt-4',
        messages: [
          {
            role: 'system',
            content: 'You are a risk assessment specialist. Provide thorough risk evaluations with actionable mitigation strategies in valid JSON format.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.3,
        max_tokens: 1500
      });

      const riskAnalysis = JSON.parse(response.choices[0].message.content);
      riskAnalysis.timestamp = new Date().toISOString();
      riskAnalysis.model_used = 'gpt-4';
      
      return riskAnalysis;
    } catch (error) {
      console.error('Risk assessment error:', error);
      return {
        error: 'Risk assessment failed',
        message: error.message,
        overall_risk: 'unknown',
        confidence_level: 0
      };
    }
  }

  async generateBooleanString(platform, role, market, skills) {
    try {
      const prompt = `Generate an optimized boolean search string for ${platform} to find ${role} candidates in ${market} market with skills: ${skills.join(', ')}.
      
      Consider platform-specific syntax and cultural context for the target market.
      Provide the result in JSON format:
      {
        "boolean_string": "optimized search string",
        "explanation": "why this string is effective",
        "alternative_strings": ["alternative1", "alternative2"],
        "platform_tips": ["tip1", "tip2"]
      }`;

      const response = await this.client.chat.completions.create({
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'system',
            content: 'You are an expert in recruitment sourcing and boolean search optimization.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.4,
        max_tokens: 800
      });

      return JSON.parse(response.choices[0].message.content);
    } catch (error) {
      console.error('Boolean string generation error:', error);
      return {
        error: 'Boolean string generation failed',
        boolean_string: '',
        explanation: error.message
      };
    }
  }

  async batchAnalysis(candidates, options = {}) {
    const results = [];
    const batchSize = options.batchSize || 5;
    
    for (let i = 0; i < candidates.length; i += batchSize) {
      const batch = candidates.slice(i, i + batchSize);
      const batchPromises = batch.map(async (candidate) => {
        try {
          const culturalAnalysis = await this.analyzeCulturalFit(
            candidate.profile,
            candidate.targetMarket,
            candidate.companyStage
          );
          
          const technicalAnalysis = await this.analyzeTechnicalProfile(
            candidate.githubData,
            candidate.linkedinData,
            candidate.targetRole
          );
          
          const riskAssessment = await this.assessRisk(
            candidate.profile,
            { cultural: culturalAnalysis, technical: technicalAnalysis },
            { market: candidate.targetMarket, role: candidate.targetRole }
          );
          
          return {
            candidate_id: candidate.id,
            cultural_analysis: culturalAnalysis,
            technical_analysis: technicalAnalysis,
            risk_assessment: riskAssessment,
            overall_score: this.calculateOverallScore(culturalAnalysis, technicalAnalysis, riskAssessment),
            processing_time: new Date().toISOString()
          };
        } catch (error) {
          return {
            candidate_id: candidate.id,
            error: 'Processing failed',
            message: error.message
          };
        }
      });
      
      const batchResults = await Promise.all(batchPromises);
      results.push(...batchResults);
      
      // Add delay between batches to respect rate limits
      if (i + batchSize < candidates.length) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    
    return results;
  }

  calculateOverallScore(cultural, technical, risk) {
    if (cultural.error || technical.error || risk.error) {
      return 0;
    }
    
    const culturalWeight = 0.4;
    const technicalWeight = 0.4;
    const riskWeight = 0.2;
    
    const riskPenalty = risk.overall_risk === 'high' ? 20 : 
                       risk.overall_risk === 'medium' ? 10 : 0;
    
    const score = (
      (cultural.cultural_score * culturalWeight) +
      (technical.technical_score * technicalWeight) +
      ((100 - riskPenalty) * riskWeight)
    );
    
    return Math.round(Math.max(0, Math.min(100, score)));
  }

  // Cost optimization methods
  estimateCost(operation, count = 1) {
    const costs = {
      cultural_analysis: 0.03, // ~$0.03 per analysis
      technical_analysis: 0.05, // ~$0.05 per analysis
      risk_assessment: 0.02,   // ~$0.02 per analysis
      boolean_generation: 0.01, // ~$0.01 per generation
      batch_analysis: 0.10     // ~$0.10 per candidate (all analyses)
    };
    
    return (costs[operation] || 0) * count;
  }

  getUsageStats() {
    // In a real implementation, this would track actual usage
    return {
      total_requests: 0,
      total_cost: 0,
      average_response_time: 0,
      success_rate: 0,
      last_reset: new Date().toISOString()
    };
  }
}

// Export for use in React components
export default MeUniqueOpenAIService;

// Example usage configuration
export const OPENAI_CONFIG = {
  models: {
    cultural: 'gpt-4',
    technical: 'gpt-4-turbo', 
    risk: 'gpt-4',
    sourcing: 'gpt-3.5-turbo'
  },
  optimization: {
    batch_size: 5,
    rate_limit_delay: 1000,
    max_retries: 3,
    timeout: 30000
  },
  cost_limits: {
    daily_limit: 50.00,
    per_analysis_limit: 0.50,
    batch_limit: 5.00
  }
};
