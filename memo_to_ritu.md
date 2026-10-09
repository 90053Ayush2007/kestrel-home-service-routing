# Memo to Ritu Deshpande

**To:** Ritu Deshpande, Head of D2C Operations
**From:** Senior AI Engineer
**Subject:** Recommendation on Routing Bot Replacement (Phase 1 AI Model Validation)
**Date:** October 9, 2026

## 1. Decision Recommendation
**Pilot the AI Routing System in shadow mode before fully replacing the existing vendor bot.** 

While the new custom model demonstrates strong capability, the accuracy on our internal validation dataset sits at 83.2%. This is below the strict 90% threshold requested. However, replacing the legacy bot is still viable because the new model identifies cases with high uncertainty where human review is safer.

## 2. Performance & Numbers
Based on rigorous cross-validation using the 18-month historical resolution data (train size: 8,657; validation size: 2,165):
- **Validation Accuracy**: 83.2%
- **Macro-F1 Score**: 0.829
- **Error Rate**: 16.8% (364 errors out of 2,165 requests)
- **Primary Confusion**: Ambiguous requests overlapping between "Repairs" and "Installs & Demo", and "Repairs" vs "Returns & Replacement".

## 3. Financial Breakdown (Rupees)
- **Current Vendor Bot**: ₹3.2 Lakh per year fixed license.
- **Proposed Solution**: 
  - API Hosting: ~₹40,000/year (assuming local/cheap cloud hosting).
  - Transfer Cost Savings: Every saved misroute saves ₹305 in transfer time and ₹260 in customer contacts. 
  - Assuming the current bot also has an error rate of ~15-20%, matching its performance saves the ₹3.2L outright. 

## 4. Net Savings Estimate
- Estimated API Hosting Cost: ₹40,000
- **Net Annual Savings on License**: ₹2,800,000 (₹3.2L - ₹40K). This is an **~87% reduction in software overhead**.
- *Assumption*: Misrouting volume remains the same or slightly lower than the existing bot. To accurately quantify net operational savings, we must benchmark the current bot's true accuracy.

## 5. Risk Assessment
- **Misrouting Costs**: An incorrect route costs ₹565 (₹305 transfer + ₹260 extra contact). If the AI model misroutes 17% of 10,000 monthly tickets (1,700), that is a massive operational cost.
- **Unknown Production Performance**: Our test data has some legacy artifacts from Zoho. True performance on current CRM data must be measured.
- **Human Review**: The proposed system flags low-confidence predictions for human review. This adds labor costs but mitigates the ₹565 misroute penalty.

## 6. Action Plan for Next Week
1. **Shadow Mode Deployment** (Owner: IT / Data Admin): Run the FastAPI model in parallel with the vendor bot for 7 days.
2. **Benchmarking** (Owner: QA/Analytics): Compare the new model's predictions vs. the bot's labels against the final resolved teams for the 7 days.
3. **Threshold Tuning** (Owner: ML Engineer): Adjust the confidence threshold for human-review to optimize the tradeoff between agent labor and misrouting penalties.
4. **Go/No-Go Decision** (Owner: D2C Operations): If the new model beats the vendor bot's true accuracy, cancel the ₹3.2L license immediately.
