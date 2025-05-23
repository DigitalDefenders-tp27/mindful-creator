# மைண்ட்ஃபுல் கிரியேட்டர் ஆப்

உள்ளடக்க உருவாக்குநர்கள் தங்கள் உள்ளடக்கத்தை நிர்வகிக்கவும், தங்கள் பார்வையாளர்களுடன் பொறுப்புடன் ஈடுபடவும் உதவும் Vue.js பயன்பாடு.

## அம்சங்கள்

- **நெறிமுறை வழிகாட்டுதல்கள்**: பொறுப்பான உள்ளடக்க உருவாக்கத்திற்கான விரிவான வழிகாட்டுதல்கள்
- **பார்வையாளர் ஈடுபாடு**: உங்கள் பார்வையாளர்களுடன் அர்த்தமுள்ள தொடர்புக்கான கருவிகள்
- **உள்ளடக்க மேலாண்மை**: உங்கள் உள்ளடக்கத்தை நெறிமுறைப்படி ஒழுங்கமைத்து திட்டமிடுங்கள்
- **பகுப்பாய்வு**: உங்கள் தாக்கத்தையும் பார்வையாளர் வளர்ச்சியையும் கண்காணிக்கவும்
- **ஓய்வு மண்டலம்**: உள்ளடக்க உருவாக்குநர்கள் மன நலத்தைப் பராமரிக்க உதவும் செயல்பாடுகள்
- **விமர்சன பதில்**: கருத்துக்களையும் விமர்சனங்களையும் கையாளுவதற்கான கருவிகள்
- **நினைவக பொருத்த விளையாட்டு**: உண்மையான மீம் படங்களைப் பயன்படுத்தி மன ஓய்வெடுக்க ஒரு சுவாரஸ்யமான விளையாட்டு

## முன் தேவைகள்

- Node.js (v16 அல்லது அதற்கு மேற்பட்ட)
- npm (v7 அல்லது அதற்கு மேற்பட்ட)
- Python 3.9+ (பின்புறத்திற்கு)

## நிறுவல்

1. களஞ்சியத்தை குளோன் செய்யவும்
   ```bash
   git clone https://github.com/DigitalDefenders-tp27/mindful-creator.git
   cd mindful-creator
   ```

2. முன்புற சார்புகளை நிறுவவும்
   ```bash
   cd frontend
   npm install
   ```

3. பின்புற சார்புகளை நிறுவவும்
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. உருவாக்க சேவையகத்தைத் தொடங்கவும்

   முன்புறம்:
   ```bash
   cd frontend
   npm run dev
   ```

   பின்புறம்:
   ```bash
   cd backend
   python run_server.py
   ```

## திட்ட அமைப்பு

```
mindful-creator/
├── frontend/                # முன்நிலை குறியீடு
│   ├── public/              # நிலையான சொத்துக்கள்
│   │   ├── icons/           # UI ஐகான்கள்
│   │   ├── media/           # ஊடக கோப்புகள்
│   │   ├── memes/           # மீம் படங்கள் (விளையாட்டுகளுக்கான)
│   │   └── emojis/          # உணர்ச்சி எமோஜிகள்
│   ├── src/                 # மூல கோப்புகள்
│   │   ├── assets/          # படங்கள், ஐகான்கள், முதலியன
│   │   ├── components/      # Vue கூறுகள்
│   │   │   ├── ui/          # UI கூறுகள்
│   │   │   ├── Activities/  # ஓய்வு செயல்பாடுகள்
│   │   │   └── Games/       # விளையாட்டு கூறுகள்
│   │   ├── content/         # உள்ளடக்க கோப்புகள்
│   │   ├── lib/             # பயன்பாட்டு நூலகங்கள்
│   │   ├── router/          # Vue ரூட்டர் கட்டமைப்பு
│   │   ├── stores/          # Pinia ஸ்டோர்கள்
│   │   ├── styles/          # உலகளாவிய பாணிகள்
│   │   ├── views/           # பக்க கூறுகள்
│   │   ├── App.vue          # ரூட் கூறு
│   │   └── main.js          # நுழைவு புள்ளி
│   └── vite.config.js       # Vite கட்டமைப்பு
├── backend/                 # பின்புற குறியீடு
│   ├── app/                 # முக்கிய பயன்பாடு
│   │   ├── api/             # API முனைப்புகள்
│   │   ├── routers/         # வழி கையாளுபவர்கள்
│   │   └── main.py          # முக்கிய பயன்பாட்டு கோப்பு
│   ├── models/              # தரவு மாதிரிகள்
│   ├── scripts/             # பயன்பாட்டு ஸ்கிரிப்ட்கள்
│   ├── requirements.txt     # பைதான் சார்புகள்
│   └── run_server.py        # சேவையக இயக்கி
└── README.md                # திட்ட ஆவணங்கள்
```

## முக்கிய பிரிவுகள்

### நெறிமுறை செல்வாக்காளர்
நம்பகத்தன்மை மூலம் நம்பிக்கையை உருவாக்குவது மற்றும் நேர்மறையான தாக்கத்தை ஏற்படுத்தும் உள்ளடக்கத்தை உருவாக்குவது பற்றி அறிந்து கொள்ளுங்கள்.

### விமர்சன பதில்
கருத்துக்களை வளர்ச்சியாக மாற்றி, சைபர்புல்லியிங்கில் இருந்து உங்களைப் பாதுகாத்துக் கொள்ளுங்கள், YouTube கருத்துகளை பகுப்பாய்வு செய்ய மற்றும் பொருத்தமான பதில்களை உருவாக்க கருவிகளைப் பயன்படுத்துங்கள்.

### ஓய்வு மண்டலம்
பல்வேறு ஓய்வு செயல்பாடுகளுடன் மன மீட்டமைப்புக்கான அமைதியான தருணங்கள், உள்ளடக்கியவை:
- சுவாசப் பயிற்சிகள்
- வழிகாட்டப்பட்ட தியானம்
- உணர்ச்சி நிலைநிறுத்தல்
- இயற்கை ஒலிகள்
- நீட்சி உடற்பயிற்சிகள்
- வண்ண சுவாசம்
- உறுதிமொழி பிரதிபலிப்பு
- குறிப்பேடு எழுதுதல்

### நினைவக பொருத்த விளையாட்டு
Memotion தரவுத்தொகுப்பிலிருந்து உண்மையான மீம்களைப் பயன்படுத்தி மன ஓய்விற்கான ஒரு சுவாரஸ்யமான மீம் பொருத்தும் விளையாட்டு.

## பயன்படுத்தப்படும் தொழில்நுட்பங்கள்

### முன்புறம்
- **கட்டமைப்பு**: Vue.js 3.5
- **நிலை மேலாண்மை**: Pinia 3.0
- **வழித்தடம்**: Vue Router 4.3
- **UI கூறுகள்**: 
  - Tailwind CSS 3.4
  - Headless UI
  - Lucide ஐகான்கள்
- **விளக்கப்படங்கள் & காட்சிப்படுத்துதல்கள்**:
  - ApexCharts 4.7
  - Chart.js 4.4
- **உருவாக்க கருவிகள்**: 
  - Vite 6.2
  - PostCSS 8.5
  - Autoprefixer 10.4

### பின்புறம்
- **கட்டமைப்பு**: FastAPI 0.95
- **தரவுத்தளம்**: SQLite/PostgreSQL மற்றும் SQLAlchemy 2.0
- **அங்கீகாரம்**: JWT
- **தரவு செயலாக்கம்**: 
  - NumPy
  - Pandas 2.1
  - TensorFlow 2.15
  - scikit-learn 1.2
- **இயற்கை மொழி செயலாக்கம்**:
  - NLTK 3.8
  - Transformers 4.30

## பதிவேற்றம்

இந்த பயன்பாட்டை பின்வரும் முறைகளில் பதிவேற்றலாம்:
- Railway
- Vercel
- Docker

Railway-இல் பதிவேற்றத்திற்கு:
1. முன்புற மற்றும் பின்புற சேவைகளுடன் Railway திட்டத்தை உள்ளமைக்கவும்
2. பொருத்தமான சூழல் மாறிகளை அமைக்கவும்
3. மீம் தரவுத்தொகுப்பு சரியாக உள்ளமைக்கப்பட்டுள்ளதா என்பதை உறுதிப்படுத்தவும்

## நன்றி தெரிவிப்புகள்

- அனைத்து குழு உறுப்பினர்களுக்கும் நன்றி
- எங்கள் ஆசிரியர்கள் மற்றும் தொழில்துறை வழிகாட்டிகளுக்கு சிறப்பு நன்றி
- பல்வேறு ஆதாரங்களிலிருந்து ஐகான் மற்றும் வடிவமைப்பு ஆதாரங்கள்

---

*இந்த திட்டம் ஆஸ்திரேலியா மற்றும் உலகெங்கிலும் உள்ள உள்ளடக்க உருவாக்குநர்கள் தங்கள் பார்வையாளர்களுடன் ஈடுபடும்போது நெறிமுறை நடைமுறைகளையும் உணர்ச்சி நலனையும் பராமரிக்க ஆதரவளிக்க வடிவமைக்கப்பட்டுள்ளது.* 