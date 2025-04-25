import { defineStore } from 'pinia'

export const useAnalysisStore = defineStore('analysis', {
  state: () => ({
    data: null
  }),

  actions: {
    set(payload) {
      // Safely transform the API data
      const toxicityDetails = payload.analysis?.toxicity_details || {}
      
      this.data = {
        analysis: {
          input_text: payload.analysis?.input_text || '',
          predicted_sentiment: payload.analysis?.predicted_sentiment || 'Unknown',
          sentiment_confidence: parseFloat(payload.analysis?.sentiment_confidence || 0),
          toxicity_details: {
            toxic: this.getToxicityDetail(toxicityDetails.toxic),
            severe_toxic: this.getToxicityDetail(toxicityDetails.severe_toxic),
            obscene: this.getToxicityDetail(toxicityDetails.obscene),
            threat: this.getToxicityDetail(toxicityDetails.threat),
            insult: this.getToxicityDetail(toxicityDetails.insult),
            identity_hate: this.getToxicityDetail(toxicityDetails.identity_hate) // Note the mapping
          }
        },
        strategy: payload.strategy || ''
      }
    },
    
    getToxicityDetail(detail) {
      return {
        prediction: detail?.prediction || 'Unknown',
        probability: parseFloat(detail?.probability || 0)
      }
    },
    
    clear() {
      this.data = null
    }
  },

  getters: {
    hasData: (state) => state.data !== null
  }
})