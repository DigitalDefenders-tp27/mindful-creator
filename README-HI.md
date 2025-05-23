# माइंडफुल क्रिएटर ऐप

कंटेंट क्रिएटर्स के लिए एक Vue.js एप्लिकेशन जो अपनी सामग्री का प्रबंधन करने और अपने दर्शकों के साथ जिम्मेदारी से जुड़ने के लिए बनाया गया है।

## विशेषताएँ

- **नैतिक दिशानिर्देश**: जिम्मेदार सामग्री निर्माण के लिए व्यापक दिशानिर्देश
- **दर्शक जुड़ाव**: अपने दर्शकों के साथ सार्थक बातचीत के लिए उपकरण
- **सामग्री प्रबंधन**: अपनी सामग्री को नैतिक रूप से व्यवस्थित और अनुसूचित करें
- **विश्लेषण**: अपने प्रभाव और दर्शक वृद्धि को ट्रैक करें
- **आराम क्षेत्र**: कंटेंट क्रिएटर्स को मानसिक स्वास्थ्य बनाए रखने में मदद करने वाली गतिविधियाँ
- **आलोचनात्मक प्रतिक्रिया**: प्रतिक्रिया और आलोचना को संभालने के लिए उपकरण
- **मेमोरी मैच गेम**: वास्तविक मीम छवियों का उपयोग करके मानसिक ब्रेक लेने के लिए एक मजेदार गेम

## आवश्यकताएँ

- Node.js (v16 या उच्चतर)
- npm (v7 या उच्चतर)
- Python 3.9+ (बैकएंड के लिए)

## स्थापना

1. रिपॉजिटरी को क्लोन करें
   ```bash
   git clone https://github.com/DigitalDefenders-tp27/mindful-creator.git
   cd mindful-creator
   ```

2. फ्रंटएंड निर्भरताओं को स्थापित करें
   ```bash
   cd frontend
   npm install
   ```

3. बैकएंड निर्भरताओं को स्थापित करें
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. विकास सर्वर प्रारंभ करें

   फ्रंटएंड:
   ```bash
   cd frontend
   npm run dev
   ```

   बैकएंड:
   ```bash
   cd backend
   python run_server.py
   ```

## प्रोजेक्ट संरचना

```
mindful-creator/
├── frontend/                # फ्रंटएंड कोड
│   ├── public/              # स्थिर संपत्तियां
│   │   ├── icons/           # UI आइकन
│   │   ├── media/           # मीडिया फाइलें
│   │   ├── memes/           # मीम छवियां (गेम के लिए)
│   │   └── emojis/          # भावना इमोजी
│   ├── src/                 # स्रोत फाइलें
│   │   ├── assets/          # चित्र, आइकन, आदि
│   │   ├── components/      # Vue कंपोनेंट्स
│   │   │   ├── ui/          # UI कंपोनेंट्स
│   │   │   ├── Activities/  # आराम गतिविधियाँ
│   │   │   └── Games/       # गेम कंपोनेंट्स
│   │   ├── content/         # सामग्री फाइलें
│   │   ├── lib/             # उपयोगिता लाइब्रेरी
│   │   ├── router/          # Vue Router कॉन्फिगरेशन
│   │   ├── stores/          # Pinia स्टोर्स
│   │   ├── styles/          # वैश्विक शैलियाँ
│   │   ├── views/           # पेज कंपोनेंट्स
│   │   ├── App.vue          # रूट कंपोनेंट
│   │   └── main.js          # प्रवेश बिंदु
│   └── vite.config.js       # Vite कॉन्फिगरेशन
├── backend/                 # बैकएंड कोड
│   ├── app/                 # मुख्य एप्लिकेशन
│   │   ├── api/             # API एंडपॉइंट्स
│   │   ├── routers/         # रूट हैंडलर्स
│   │   └── main.py          # मुख्य एप्लिकेशन फाइल
│   ├── models/              # डेटा मॉडल्स
│   ├── scripts/             # उपयोगिता स्क्रिप्ट्स
│   ├── requirements.txt     # पाइथन निर्भरताएँ
│   └── run_server.py        # सर्वर रनर
└── README.md                # प्रोजेक्ट दस्तावेज़ीकरण
```

## प्रमुख अनुभाग

### नैतिक प्रभावकर्ता
प्रामाणिकता के माध्यम से विश्वास बनाने और सकारात्मक प्रभाव डालने वाली सामग्री बनाने के बारे में जानें।

### आलोचनात्मक प्रतिक्रिया
प्रतिक्रिया को विकास में बदलें और साइबरबुलिंग से खुद को बचाएं, YouTube टिप्पणियों का विश्लेषण करने और उचित प्रतिक्रिया विकसित करने के लिए उपकरणों का उपयोग करें।

### आराम क्षेत्र
विभिन्न आराम गतिविधियों के साथ मानसिक विश्राम के लिए शांतिपूर्ण क्षण, जिनमें शामिल हैं:
- श्वास व्यायाम
- गाइडेड ध्यान
- संवेदी ग्राउंडिंग
- प्रकृति ध्वनियाँ
- स्ट्रेचिंग रूटीन
- रंग श्वास
- सकारात्मक पुष्टि प्रतिबिंब
- जर्नलिंग

### मेमोरी मैच गेम
एक मज़ेदार मीम मिलान गेम जो Memotion डेटासेट से वास्तविक मीम का उपयोग करते हुए मानसिक ब्रेक प्रदान करता है।

## प्रयुक्त तकनीकें

### फ्रंटएंड
- **फ्रेमवर्क**: Vue.js 3.5
- **स्टेट मैनेजमेंट**: Pinia 3.0
- **राउटिंग**: Vue Router 4.3
- **UI कंपोनेंट्स**: 
  - Tailwind CSS 3.4
  - Headless UI
  - Lucide आइकन्स
- **चार्ट्स और विज़ुअलाइज़ेशन**:
  - ApexCharts 4.7
  - Chart.js 4.4
- **बिल्ड टूल्स**: 
  - Vite 6.2
  - PostCSS 8.5
  - Autoprefixer 10.4

### बैकएंड
- **फ्रेमवर्क**: FastAPI 0.95
- **डेटाबेस**: SQLite/PostgreSQL विद SQLAlchemy 2.0
- **प्रमाणीकरण**: JWT
- **डेटा प्रोसेसिंग**: 
  - NumPy
  - Pandas 2.1
  - TensorFlow 2.15
  - scikit-learn 1.2
- **नेचुरल लैंग्वेज प्रोसेसिंग**:
  - NLTK 3.8
  - Transformers 4.30

## डिप्लॉयमेंट

इस एप्लिकेशन को निम्न के माध्यम से डिप्लॉय किया जा सकता है:
- Railway
- Vercel
- Docker

Railway पर डिप्लॉयमेंट के लिए:
1. फ्रंटएंड और बैकएंड सेवाओं के साथ Railway प्रोजेक्ट कॉन्फ़िगर करें
2. उचित पर्यावरण चर सेट करें
3. सुनिश्चित करें कि मीम डेटासेट सही ढंग से कॉन्फ़िगर किया गया है

## आभार

- सभी टीम सदस्यों को धन्यवाद
- हमारे शिक्षकों और औद्योगिक मेंटर्स को विशेष धन्यवाद
- विभिन्न स्रोतों से आइकन और डिज़ाइन संसाधन

---

*यह प्रोजेक्ट ऑस्ट्रेलिया और दुनिया भर के कंटेंट क्रिएटर्स को अपने दर्शकों के साथ जुड़ते समय नैतिक प्रथाओं और भावनात्मक स्वास्थ्य को बनाए रखने में सहायता करने के लिए डिज़ाइन किया गया है।* 