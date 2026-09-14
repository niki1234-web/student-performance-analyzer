from database import get_db, init_indexes, upsert_subject, upsert_topic


SAMPLE_DATA = {
    # ==================== PRIMARY (1-5) ====================
    "Primary (1-5)": {
        "General": {
            "English": [
                ("Which is a vowel?", ["A", "B", "C", "D"], "A", "Easy"),
                ("How many letters in English alphabet?", ["24", "25", "26", "27"], "26", "Easy"),
                ("Which word is a noun?", ["Run", "Cat", "Quickly", "Jump"], "Cat", "Easy"),
                ("Opposite of 'big'?", ["Tall", "Small", "Wide", "Huge"], "Small", "Easy"),
                ("Plural of 'child'?", ["Childs", "Childes", "Children", "Child"], "Children", "Medium"),
            ],
            "Hindi": [
                ("'आ' कौन सा स्वर है?", ["ह्रस्व", "दीर्घ", "प्लुत", "अयोगवाह"], "दीर्घ", "Easy"),
                ("'क' कौन सा व्यंजन है?", ["स्पर्श", "अंतःस्थ", "ऊष्म", "स्वर"], "स्पर्श", "Easy"),
                ("'माता' का पर्यायवाची?", ["पिता", "भाई", "माँ", "बहन"], "माँ", "Easy"),
                ("विलोम शब्द 'दिन'?", ["रात", "सुबह", "शाम", "दोपहर"], "रात", "Easy"),
                ("'बच्चा' का बहुवचन?", ["बच्चे", "बच्चों", "बच्चा", "बच्ची"], "बच्चे", "Medium"),
            ],
            "Maths": [
                ("2 + 3 = ?", ["4", "5", "6", "7"], "5", "Easy"),
                ("10 - 4 = ?", ["5", "6", "7", "8"], "6", "Easy"),
                ("5 × 2 = ?", ["8", "10", "12", "15"], "10", "Easy"),
                ("12 ÷ 3 = ?", ["3", "4", "5", "6"], "4", "Easy"),
                ("How many sides in a triangle?", ["2", "3", "4", "5"], "3", "Easy"),
            ],
            "EVS": [
                ("Which animal gives us milk?", ["Cow", "Dog", "Cat", "Lion"], "Cow", "Easy"),
                ("What do plants need to grow?", ["Water", "Plastic", "Stone", "Metal"], "Water", "Easy"),
                ("Which is a fruit?", ["Carrot", "Apple", "Potato", "Onion"], "Apple", "Easy"),
                ("How many days in a week?", ["5", "6", "7", "8"], "7", "Easy"),
                ("Which is our national bird?", ["Crow", "Peacock", "Parrot", "Sparrow"], "Peacock", "Medium"),
            ],
            "GK": [
                ("What is the capital of India?", ["Mumbai", "Delhi", "Kolkata", "Chennai"], "Delhi", "Easy"),
                ("How many colors in a rainbow?", ["5", "6", "7", "8"], "7", "Easy"),
                ("Which is the national animal?", ["Lion", "Tiger", "Elephant", "Bear"], "Tiger", "Easy"),
                ("How many players in cricket team?", ["9", "10", "11", "12"], "11", "Easy"),
                ("Who is the father of our nation?", ["Nehru", "Gandhi", "Patel", "Bose"], "Gandhi", "Medium"),
            ],
        },
    },
    
    # ==================== MIDDLE (6-8) ====================
    "Middle (6-8)": {
        "General": {
            "English": [
                ("Identify the verb: She sings well.", ["She", "sings", "well", "None"], "sings", "Easy"),
                ("Plural of 'mouse'?", ["mouses", "mice", "mouse", "mices"], "mice", "Easy"),
                ("Synonym of 'happy'?", ["Sad", "Joyful", "Angry", "Tired"], "Joyful", "Easy"),
                ("Past tense of 'go'?", ["goed", "goes", "went", "gone"], "went", "Medium"),
                ("Antonym of 'ancient'?", ["Old", "Modern", "Historic", "Past"], "Modern", "Medium"),
            ],
            "Hindi": [
                ("'सूर्य' का पर्यायवाची?", ["चंद्र", "रवि", "तारा", "आकाश"], "रवि", "Easy"),
                ("'अच्छा' का विलोम?", ["अच्छा", "बुरा", "सुंदर", "मीठा"], "बुरा", "Easy"),
                ("व्याकरण में 'लिंग' कितने प्रकार?", ["एक", "दो", "तीन", "चार"], "दो", "Easy"),
                ("'किताब' का बहुवचन?", ["किताबें", "किताबे", "किताबों", "किताबा"], "किताबें", "Medium"),
                ("'रहना' कौन सी क्रिया है?", ["सकर्मक", "अकर्मक", "प्रेरणार्थक", "संयुक्त"], "अकर्मक", "Hard"),
            ],
            "Maths": [
                ("LCM of 4 and 6?", ["8", "10", "12", "24"], "12", "Easy"),
                ("Area of a square with side 5?", ["10", "15", "20", "25"], "25", "Easy"),
                ("Solve: 3x = 12", ["3", "4", "5", "6"], "4", "Easy"),
                ("Perimeter of rectangle 5×3?", ["8", "12", "16", "20"], "16", "Medium"),
                ("45 ÷ 9 = ?", ["4", "5", "6", "7"], "5", "Easy"),
            ],
            "Science": [
                ("Photosynthesis happens in?", ["Roots", "Stem", "Leaves", "Flower"], "Leaves", "Easy"),
                ("SI unit of length?", ["cm", "m", "km", "mm"], "m", "Easy"),
                ("H2O is?", ["Salt", "Sugar", "Water", "Air"], "Water", "Easy"),
                ("Which gas we breathe in?", ["CO2", "O2", "N2", "H2"], "O2", "Easy"),
                ("Force unit in SI?", ["Joule", "Newton", "Watt", "Pascal"], "Newton", "Medium"),
            ],
            "SST": [
                ("Who built the Taj Mahal?", ["Akbar", "Shah Jahan", "Aurangzeb", "Babur"], "Shah Jahan", "Easy"),
                ("Largest continent?", ["Asia", "Africa", "Europe", "America"], "Asia", "Easy"),
                ("Capital of France?", ["London", "Paris", "Berlin", "Rome"], "Paris", "Easy"),
                ("Who was the first PM of India?", ["Gandhi", "Nehru", "Patel", "Bose"], "Nehru", "Easy"),
                ("Which is the longest river in India?", ["Yamuna", "Ganga", "Godavari", "Narmada"], "Ganga", "Medium"),
            ],
        },
    },
    
    # ==================== SECONDARY (9-10) ====================
    "Secondary (9-10)": {
        "General": {
            "Mathematics": [
                ("Factorize: x² - 4", ["(x-2)(x+2)", "(x-4)(x+1)", "(x-1)(x+4)", "x(x-4)"], "(x-2)(x+2)", "Medium"),
                ("sin²θ + cos²θ = ?", ["0", "1", "2", "tan θ"], "1", "Easy"),
                ("Quadratic formula is:", ["-b/2a", "(-b±√(b²-4ac))/2a", "b²-4ac", "-b/a"], "(-b±√(b²-4ac))/2a", "Medium"),
                ("Sum of angles of triangle?", ["90°", "180°", "270°", "360°"], "180°", "Easy"),
                ("Value of π (approximately)?", ["2.14", "3.14", "4.14", "1.14"], "3.14", "Easy"),
            ],
            "Science": [
                ("SI unit of Force?", ["Joule", "Newton", "Watt", "Pascal"], "Newton", "Easy"),
                ("Chemical formula of water?", ["H2O", "CO2", "O2", "H2O2"], "H2O", "Easy"),
                ("Photosynthesis produces?", ["CO2", "O2", "N2", "H2"], "O2", "Easy"),
                ("Ohm's law?", ["V=IR", "P=VI", "F=ma", "E=mc²"], "V=IR", "Medium"),
                ("Basic unit of life?", ["Atom", "Cell", "Molecule", "Organ"], "Cell", "Easy"),
            ],
            "English": [
                ("Synonym of 'brave'?", ["Coward", "Bold", "Weak", "Timid"], "Bold", "Easy"),
                ("Antonym of 'victory'?", ["Win", "Defeat", "Success", "Triumph"], "Defeat", "Easy"),
                ("Identify the noun: 'The dog barked.'", ["The", "dog", "barked", "None"], "dog", "Easy"),
                ("Past tense of 'write'?", ["writed", "wrote", "written", "writes"], "wrote", "Medium"),
                ("'Beautiful' is a?", ["Noun", "Verb", "Adjective", "Adverb"], "Adjective", "Easy"),
            ],
            "Hindi": [
                ("'नदी' का पर्यायवाची?", ["सरिता", "पर्वत", "सागर", "तालाब"], "सरिता", "Easy"),
                ("'अंधकार' का विलोम?", ["प्रकाश", "रात", "काला", "छाया"], "प्रकाश", "Easy"),
                ("संधि कितने प्रकार की होती है?", ["दो", "तीन", "चार", "पाँच"], "तीन", "Medium"),
                ("'राम' कौन सा लिंग है?", ["स्त्रीलिंग", "पुल्लिंग", "नपुंसक", "उभय"], "पुल्लिंग", "Easy"),
                ("समास कितने प्रकार?", ["चार", "छह", "आठ", "दस"], "छह", "Hard"),
            ],
            "SST": [
                ("When did India get independence?", ["1945", "1946", "1947", "1948"], "1947", "Easy"),
                ("Who wrote the Constitution of India?", ["Nehru", "Dr. Ambedkar", "Patel", "Gandhi"], "Dr. Ambedkar", "Medium"),
                ("French Revolution year?", ["1776", "1789", "1800", "1815"], "1789", "Medium"),
                ("Which is the largest democracy?", ["USA", "India", "China", "Russia"], "India", "Easy"),
                ("The Great Wall is in?", ["Japan", "China", "Korea", "Mongolia"], "China", "Easy"),
            ],
        },
    },
    
    # ==================== SENIOR SECONDARY — SCIENCE (11-12) ====================
    "Senior Secondary (11-12)": {
        "Science": {
            "Physics": [
                ("Unit of electric current?", ["Volt", "Ampere", "Ohm", "Watt"], "Ampere", "Easy"),
                ("Newton's second law: F = ?", ["ma", "mv", "mgh", "mc²"], "ma", "Easy"),
                ("Speed of light?", ["3×10⁶ m/s", "3×10⁸ m/s", "3×10¹⁰ m/s", "3×10⁵ m/s"], "3×10⁸ m/s", "Medium"),
                ("SI unit of energy?", ["Newton", "Joule", "Watt", "Pascal"], "Joule", "Easy"),
                ("Ohm's law?", ["V=IR", "P=VI", "F=ma", "E=mc²"], "V=IR", "Easy"),
            ],
            "Chemistry": [
                ("Atomic number of Carbon?", ["4", "6", "8", "12"], "6", "Easy"),
                ("Chemical formula of glucose?", ["C6H12O6", "C2H5OH", "CH4", "CO2"], "C6H12O6", "Medium"),
                ("pH of neutral solution?", ["5", "6", "7", "8"], "7", "Easy"),
                ("Noble gas?", ["Oxygen", "Nitrogen", "Helium", "Hydrogen"], "Helium", "Easy"),
                ("Bond in NaCl?", ["Covalent", "Ionic", "Metallic", "Hydrogen"], "Ionic", "Medium"),
            ],
            "Mathematics": [
                ("Derivative of sin x?", ["cos x", "-cos x", "sin x", "-sin x"], "cos x", "Medium"),
                ("∫ x dx = ?", ["x²", "x²/2 + C", "2x + C", "x + C"], "x²/2 + C", "Medium"),
                ("Value of e?", ["2.71", "3.14", "1.61", "1.41"], "2.71", "Easy"),
                ("Probability of certain event?", ["0", "0.5", "1", "∞"], "1", "Easy"),
                ("Limit of 1/x as x→∞?", ["0", "1", "∞", "undefined"], "0", "Medium"),
            ],
            "Biology": [
                ("Powerhouse of cell?", ["Nucleus", "Mitochondria", "Ribosome", "Chloroplast"], "Mitochondria", "Easy"),
                ("Photosynthesis takes place in?", ["Mitochondria", "Chloroplast", "Nucleus", "Vacuole"], "Chloroplast", "Easy"),
                ("Blood groups in humans?", ["2", "3", "4", "5"], "4", "Medium"),
                ("DNA stands for?", ["Deoxyribonucleic Acid", "Dinucleic Acid", "Deoxyribose Acid", "None"], "Deoxyribonucleic Acid", "Easy"),
                ("Human body chromosomes?", ["23", "46", "44", "22"], "46", "Medium"),
            ],
            "Computer Science": [
                ("Binary of 5?", ["100", "101", "110", "111"], "101", "Easy"),
                ("Full form of CPU?", ["Central Processing Unit", "Computer Personal Unit", "Central Program Unit", "None"], "Central Processing Unit", "Easy"),
                ("HTML stands for?", ["Hyper Text Markup Language", "High Text Machine Language", "Hyper Text Machine Language", "None"], "Hyper Text Markup Language", "Easy"),
                ("Which is not a programming language?", ["Python", "Java", "HTML", "C++"], "HTML", "Medium"),
                ("RAM is?", ["Permanent", "Temporary", "Secondary", "External"], "Temporary", "Easy"),
            ],
            "English": [
                ("Synonym of 'ephemeral'?", ["Permanent", "Short-lived", "Eternal", "Long"], "Short-lived", "Hard"),
                ("Antonym of 'benevolent'?", ["Kind", "Cruel", "Gentle", "Nice"], "Cruel", "Medium"),
                ("Identify the figure of speech: 'Time is a thief.'", ["Simile", "Metaphor", "Personification", "Alliteration"], "Metaphor", "Medium"),
                ("'Ubiquitous' means?", ["Rare", "Present everywhere", "Ancient", "Modern"], "Present everywhere", "Hard"),
                ("Correct spelling?", ["Recieve", "Receive", "Receeve", "Receve"], "Receive", "Easy"),
            ],
        },
        
        # ==================== SENIOR SECONDARY — COMMERCE (11-12) ====================
        "Commerce": {
            "Accountancy": [
                ("Accounting equation?", ["Assets = Liabilities + Capital", "Assets = Liabilities - Capital", "Assets + Liabilities = Capital", "None"], "Assets = Liabilities + Capital", "Easy"),
                ("Golden rule of debit?", ["Debit what comes in", "Debit what goes out", "Debit receiver", "None"], "Debit what comes in", "Medium"),
                ("Trial balance is a?", ["Statement", "Account", "Ledger", "Journal"], "Statement", "Easy"),
                ("Depreciation is?", ["Appreciation", "Decrease in value", "Increase in value", "None"], "Decrease in value", "Easy"),
                ("Capital is a?", ["Liability", "Asset", "Income", "Expense"], "Liability", "Medium"),
            ],
            "Business Studies": [
                ("Forms of business organization?", ["Sole, Partnership, Company", "Only Company", "Only Partnership", "None"], "Sole, Partnership, Company", "Easy"),
                ("Management is?", ["Art", "Science", "Both", "None"], "Both", "Medium"),
                ("Marketing mix includes?", ["4 Ps", "3 Ps", "5 Ps", "6 Ps"], "4 Ps", "Easy"),
                ("Types of partners?", ["Active, Sleeping", "Only Active", "Only Sleeping", "None"], "Active, Sleeping", "Medium"),
                ("SEBI regulates?", ["Banks", "Stock Market", "Insurance", "NBFC"], "Stock Market", "Easy"),
            ],
            "Economics": [
                ("Law of demand?", ["Price up, demand up", "Price up, demand down", "No relation", "None"], "Price up, demand down", "Easy"),
                ("GDP stands for?", ["Gross Domestic Product", "Gross Demand Product", "Gross Development Product", "None"], "Gross Domestic Product", "Easy"),
                ("Inflation means?", ["Fall in prices", "Rise in prices", "Stable prices", "None"], "Rise in prices", "Easy"),
                ("Types of economy?", ["Capitalist, Socialist, Mixed", "Only Capitalist", "Only Socialist", "None"], "Capitalist, Socialist, Mixed", "Medium"),
                ("Opportunity cost is?", ["Next best alternative", "Total cost", "Fixed cost", "Variable cost"], "Next best alternative", "Medium"),
            ],
            "Mathematics": [
                ("Simple interest formula?", ["P×R×T/100", "P+R+T", "P×R/T", "P/R/T"], "P×R×T/100", "Easy"),
                ("Compound interest is on?", ["Principal only", "Principal + Interest", "Interest only", "None"], "Principal + Interest", "Medium"),
                ("Percentage of 50 in 200?", ["20%", "25%", "30%", "40%"], "25%", "Easy"),
                ("Ratio 2:3 total 50, first part?", ["20", "25", "30", "15"], "20", "Medium"),
                ("Profit % formula?", ["(SP-CP)/CP × 100", "(SP+CP)/CP × 100", "SP/CP × 100", "None"], "(SP-CP)/CP × 100", "Easy"),
            ],
            "English": [
                ("Synonym of 'lucrative'?", ["Loss-making", "Profitable", "Costly", "Cheap"], "Profitable", "Medium"),
                ("Business letter format?", ["Formal", "Informal", "Casual", "None"], "Formal", "Easy"),
                ("'Bankruptcy' means?", ["Profit", "Insolvency", "Investment", "Loan"], "Insolvency", "Medium"),
                ("Antonym of 'surplus'?", ["Excess", "Deficit", "Extra", "More"], "Deficit", "Medium"),
                ("'Revenue' refers to?", ["Income", "Expense", "Loss", "Debt"], "Income", "Easy"),
            ],
        },
        
        # ==================== SENIOR SECONDARY — ARTS (11-12) ====================
        "Arts": {
            "History": [
                ("Indus Valley Civilization year?", ["2500 BC", "1500 BC", "500 BC", "1000 AD"], "2500 BC", "Medium"),
                ("Who founded Mauryan Empire?", ["Ashoka", "Chandragupta Maurya", "Bindusara", "Bimbisara"], "Chandragupta Maurya", "Easy"),
                ("Battle of Plassey year?", ["1757", "1764", "1857", "1947"], "1757", "Medium"),
                ("First World War year?", ["1912", "1914", "1918", "1920"], "1914", "Easy"),
                ("Mughal Empire founder?", ["Akbar", "Babur", "Humayun", "Shah Jahan"], "Babur", "Easy"),
            ],
            "Political Science": [
                ("Preamble starts with?", ["We the People", "We the Nation", "We the Citizens", "None"], "We the People", "Easy"),
                ("Fundamental Rights are in?", ["Part III", "Part II", "Part IV", "Part V"], "Part III", "Medium"),
                ("Article 21 is about?", ["Equality", "Right to Life", "Freedom", "Religion"], "Right to Life", "Medium"),
                ("Rajya Sabha members?", ["250", "245", "238", "240"], "245", "Medium"),
                ("Who is the head of state in India?", ["PM", "President", "CJI", "Speaker"], "President", "Easy"),
            ],
            "Geography": [
                ("Largest desert?", ["Sahara", "Thar", "Gobi", "Kalahari"], "Sahara", "Easy"),
                ("Longest river in world?", ["Amazon", "Nile", "Yangtze", "Mississippi"], "Nile", "Easy"),
                ("Highest mountain?", ["K2", "Everest", "Kilimanjaro", "Denali"], "Everest", "Easy"),
                ("Largest ocean?", ["Atlantic", "Indian", "Arctic", "Pacific"], "Pacific", "Easy"),
                ("India's coastline length?", ["5000 km", "6000 km", "7500 km", "8000 km"], "7500 km", "Hard"),
            ],
            "Economics": [
                ("Adam Smith wrote?", ["Wealth of Nations", "Das Kapital", "Republic", "None"], "Wealth of Nations", "Medium"),
                ("Microeconomics studies?", ["Individual units", "Whole economy", "Government", "None"], "Individual units", "Easy"),
                ("Demand curve slopes?", ["Upward", "Downward", "Vertical", "Horizontal"], "Downward", "Easy"),
                ("Monopoly means?", ["Many sellers", "One seller", "Two sellers", "No seller"], "One seller", "Easy"),
                ("Inflation impact on poor?", ["Positive", "Negative", "Neutral", "None"], "Negative", "Medium"),
            ],
            "Psychology": [
                ("Father of Psychology?", ["Freud", "Wilhelm Wundt", "Skinner", "Pavlov"], "Wilhelm Wundt", "Medium"),
                ("IQ stands for?", ["Intelligence Quotient", "Important Question", "Inner Quality", "None"], "Intelligence Quotient", "Easy"),
                ("Classical conditioning by?", ["Skinner", "Pavlov", "Freud", "Jung"], "Pavlov", "Medium"),
                ("Types of memory?", ["Sensory, Short, Long", "Only Short", "Only Long", "None"], "Sensory, Short, Long", "Hard"),
                ("Defense mechanisms are by?", ["Freud", "Jung", "Adler", "Skinner"], "Freud", "Medium"),
            ],
            "English": [
                ("Figure of speech in 'The wind whispered'?", ["Simile", "Metaphor", "Personification", "Alliteration"], "Personification", "Medium"),
                ("'Hamlet' written by?", ["Shakespeare", "Milton", "Chaucer", "Wordsworth"], "Shakespeare", "Easy"),
                ("'Ode' is a?", ["Poem", "Novel", "Play", "Essay"], "Poem", "Easy"),
                ("Synonym of 'sagacious'?", ["Foolish", "Wise", "Lazy", "Angry"], "Wise", "Hard"),
                ("Romantic age poet?", ["Pope", "Wordsworth", "Dryden", "Eliot"], "Wordsworth", "Medium"),
            ],
        },
    },
    
    # ==================== GRADUATE (UG) ====================
    "Graduate (UG)": {
        "Science": {
            "Physics": [
                ("Schrödinger equation is?", ["Quantum", "Classical", "Relativistic", "Statistical"], "Quantum", "Hard"),
                ("Lorentz transformation relates?", ["Space and time", "Mass and energy", "Force and motion", "None"], "Space and time", "Hard"),
                ("Entropy always?", ["Decreases", "Increases", "Stays same", "None"], "Increases", "Medium"),
                ("Semiconductor doping adds?", ["Neutrons", "Impurities", "Electrons only", "None"], "Impurities", "Medium"),
                ("LASER stands for?", ["Light Amplification", "Light Absorption", "Long Amplification", "None"], "Light Amplification", "Easy"),
            ],
            "Chemistry": [
                ("Molarity unit?", ["mol/L", "mol/kg", "g/L", "g/mol"], "mol/L", "Medium"),
                ("Benzene formula?", ["C6H6", "C6H12", "C5H5", "C7H8"], "C6H6", "Easy"),
                ("pH range?", ["0-7", "0-14", "1-10", "0-10"], "0-14", "Easy"),
                ("SN1 reaction order?", ["1", "2", "0", "3"], "1", "Hard"),
                ("Enzyme is a?", ["Protein", "Carbohydrate", "Lipid", "Nucleic acid"], "Protein", "Medium"),
            ],
            "Biology": [
                ("DNA replication is?", ["Conservative", "Semi-conservative", "Dispersive", "None"], "Semi-conservative", "Medium"),
                ("Mendel worked on?", ["Pea plant", "Fruit fly", "Bacteria", "None"], "Pea plant", "Easy"),
                ("Human genome has?", ["20,000-25,000 genes", "50,000 genes", "100,000 genes", "None"], "20,000-25,000 genes", "Hard"),
                ("ATP is?", ["Energy currency", "Protein", "Lipid", "Sugar"], "Energy currency", "Easy"),
                ("Enzyme function?", ["Catalysis", "Inhibition", "Transport", "None"], "Catalysis", "Medium"),
            ],
        },
        "Commerce": {
            "Financial Accounting": [
                ("GAAP stands for?", ["Generally Accepted Accounting Principles", "General Accounting", "Great Accounting", "None"], "Generally Accepted Accounting Principles", "Easy"),
                ("Balance sheet shows?", ["Assets & Liabilities", "Only Assets", "Only Liabilities", "None"], "Assets & Liabilities", "Easy"),
                ("Depreciation method?", ["Straight line", "Written down", "Both", "None"], "Both", "Medium"),
                ("Goodwill is?", ["Intangible", "Tangible", "Fixed", "Current"], "Intangible", "Medium"),
                ("Cash flow statement includes?", ["Operating, Investing, Financing", "Only Operating", "Only Investing", "None"], "Operating, Investing, Financing", "Easy"),
            ],
            "Business Law": [
                ("Indian Contract Act year?", ["1872", "1882", "1930", "1956"], "1872", "Medium"),
                ("Types of contracts?", ["Valid, Void, Voidable", "Only Valid", "Only Void", "None"], "Valid, Void, Voidable", "Easy"),
                ("Sale of Goods Act year?", ["1930", "1956", "1990", "2000"], "1930", "Medium"),
                ("Consumer Protection Act year?", ["1986", "2000", "2019", "2020"], "2019", "Hard"),
                ("Partnership Act year?", ["1932", "1956", "1990", "2000"], "1932", "Medium"),
            ],
            "Economics": [
                ("Micro vs Macro?", ["Individual vs Aggregate", "Both same", "None", "Different"], "Individual vs Aggregate", "Easy"),
                ("Elasticity of demand?", ["Responsiveness", "Fixed", "Zero", "None"], "Responsiveness", "Medium"),
                ("Market structures?", ["Perfect, Monopoly, Oligopoly", "Only Perfect", "Only Monopoly", "None"], "Perfect, Monopoly, Oligopoly", "Easy"),
                ("Fiscal policy by?", ["Government", "RBI", "Banks", "None"], "Government", "Easy"),
                ("Monetary policy by?", ["RBI", "Government", "Banks", "None"], "RBI", "Easy"),
            ],
        },
        "Arts": {
            "History": [
                ("Harappan Civilization discovered in?", ["1921", "1931", "1941", "1951"], "1921", "Medium"),
                ("Who wrote 'Discovery of India'?", ["Gandhi", "Nehru", "Patel", "Bose"], "Nehru", "Easy"),
                ("Renaissance began in?", ["France", "Italy", "England", "Germany"], "Italy", "Medium"),
                ("Industrial Revolution began in?", ["France", "England", "Germany", "USA"], "England", "Easy"),
                ("UN founded in?", ["1945", "1946", "1950", "1947"], "1945", "Easy"),
            ],
            "Political Science": [
                ("Sovereignty means?", ["Supreme power", "Division", "Limitation", "None"], "Supreme power", "Medium"),
                ("Democracy types?", ["Direct, Indirect", "Only Direct", "Only Indirect", "None"], "Direct, Indirect", "Easy"),
                ("Federalism means?", ["Two-tier govt", "Single govt", "None", "Both"], "Two-tier govt", "Medium"),
                ("Marx wrote?", ["Das Kapital", "Republic", "Leviathan", "None"], "Das Kapital", "Medium"),
                ("Liberty means?", ["Freedom", "Slavery", "Bondage", "None"], "Freedom", "Easy"),
            ],
        },
    },
    
    # ==================== POST GRADUATE (PG) ====================
    "Post Graduate (PG)": {
        "Science": {
            "Advanced Physics": [
                ("Quantum entanglement is?", ["Correlation", "Causation", "Random", "None"], "Correlation", "Hard"),
                ("General Relativity by?", ["Newton", "Einstein", "Bohr", "Feynman"], "Einstein", "Easy"),
                ("String theory requires?", ["Extra dimensions", "No dimensions", "1 dimension", "None"], "Extra dimensions", "Hard"),
                ("Higgs boson discovered in?", ["2010", "2012", "2015", "2018"], "2012", "Medium"),
                ("Standard Model describes?", ["Particles", "Forces", "Both", "None"], "Both", "Hard"),
            ],
        },
        "Commerce": {
            "Advanced Accounting": [
                ("IFRS stands for?", ["International Financial Reporting Standards", "Indian Financial Reporting", "International Finance", "None"], "International Financial Reporting Standards", "Medium"),
                ("Consolidated statements are for?", ["Group", "Single entity", "None", "Both"], "Group", "Medium"),
                ("Lease accounting standard?", ["IFRS 16", "IFRS 15", "IFRS 17", "IFRS 18"], "IFRS 16", "Hard"),
                ("Goodwill impairment test?", ["Annual", "Biennial", "Triennial", "None"], "Annual", "Hard"),
                ("ESG reporting stands for?", ["Environment, Social, Governance", "Economic, Social, Governance", "Environment, Social, Growth", "None"], "Environment, Social, Governance", "Medium"),
            ],
        },
        "Arts": {
            "Advanced History": [
                ("Post-modern history focuses on?", ["Multiple narratives", "Single truth", "None", "Both"], "Multiple narratives", "Hard"),
                ("Subaltern studies by?", ["Ranajit Guha", "Nehru", "Patel", "None"], "Ranajit Guha", "Hard"),
                ("World Systems Theory by?", ["Wallerstein", "Marx", "Weber", "Durkheim"], "Wallerstein", "Hard"),
                ("Cultural history emphasizes?", ["Lived experience", "Political events", "Economic facts", "None"], "Lived experience", "Hard"),
                ("Annales School was in?", ["France", "England", "Germany", "Italy"], "France", "Hard"),
            ],
        },
    },
}
# ============================================================
# SEED FUNCTION
# ============================================================

def seed_database(force: bool = False) -> bool:
    """Seed the database with sample subjects, topics and questions."""
    db = get_db()
    if db is None:
        return False

    init_indexes()
    if force:
        db.subjects.delete_many({})
        db.topics.delete_many({})
        db.questions.delete_many({})
    elif db.questions.count_documents({}) > 0:
        return True

    for level, streams in SAMPLE_DATA.items():
        for stream, subjects in streams.items():
            for subject_name, topics in subjects.items():
                full_subject = f"{level} / {stream} / {subject_name}"
                upsert_subject(full_subject)
                # topics is a LIST of tuples, not a dict
                for topic_tuple in topics:
                    # topic_tuple = (question_text, options, correct_answer, difficulty)
                    question_text, options, correct_answer, difficulty = topic_tuple
                    # Use subject_name as the topic (since data is flat — no subtopic)
                    topic_name = subject_name
                    upsert_topic(full_subject, topic_name)
                    db.questions.update_one(
                        {"question": question_text, "subject": full_subject, "topic": topic_name},
                        {
                            "$set": {
                                "question": question_text,
                                "options": options,
                                "correct_answer": correct_answer,
                                "subject": full_subject,
                                "topic": topic_name,
                                "difficulty": difficulty,
                            }
                        },
                        upsert=True,
                    )
    return True