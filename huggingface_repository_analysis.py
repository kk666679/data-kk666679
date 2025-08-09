#!/usr/bin/env python3
"""
HuggingFace Repository Analysis for HRMS Malaysia
Analyzes and recommends optimal models for Malaysian HR use cases
"""

from backend.integrations.huggingface_analysis import HuggingFaceAnalyzer
from backend.integrations.model_optimizer import ModelOptimizer, analyze_huggingface_repository
import json

def main():
    print("🤗 HuggingFace Repository Analysis for HRMS Malaysia")
    print("=" * 60)
    
    try:
        # Run comprehensive analysis
        analysis_results = analyze_huggingface_repository()
        
        print("\n📊 Analysis Results:")
        print(f"   Models Analyzed: {analysis_results['summary']['total_models_analyzed']}")
        print(f"   Recommendations: {analysis_results['summary']['recommended_models']}")
        print(f"   Benchmarked: {analysis_results['summary']['benchmarked_models']}")
        
        # Display recommendations
        print("\n🎯 Recommended Models for HRMS:")
        recommendations = analysis_results['repository_analysis']['recommendations']
        
        for task, details in recommendations.items():
            print(f"\n   {task.upper()}:")
            print(f"     Primary: {details['primary']}")
            print(f"     Reason: {details['reason']}")
        
        # Display benchmark results
        print("\n⚡ Performance Benchmarks:")
        benchmarks = analysis_results['repository_analysis']['performance_benchmarks']
        
        for model_id, metrics in benchmarks.items():
            if metrics.get('status') == 'success':
                print(f"\n   {model_id}:")
                print(f"     Load Time: {metrics['load_time']}s")
                print(f"     Inference: {metrics['avg_inference_time']}s")
                print(f"     Size: {metrics['model_size_mb']}MB")
        
        # Save detailed results
        with open('huggingface_analysis_results.json', 'w') as f:
            json.dump(analysis_results, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: huggingface_analysis_results.json")
        
        # Optimization recommendations
        print("\n🚀 Optimization Recommendations:")
        print("   1. Use cardiffnlp/twitter-roberta-base-sentiment-latest for sentiment analysis")
        print("   2. Implement sentence-transformers/all-MiniLM-L6-v2 for semantic search")
        print("   3. Consider model quantization for production deployment")
        print("   4. Cache model outputs for repeated queries")
        print("   5. Use GPU acceleration when available")
        
        print("\n✅ HuggingFace repository analysis completed!")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        print("   Ensure transformers and huggingface_hub are installed")

if __name__ == "__main__":
    main()