from database import get_db, init_indexes, upsert_subject, upsert_topic

SAMPLE_DATA = {
    "Mathematics": {
        "Algebra": [
            ("Solve: 2x + 5 = 15", ["x = 4", "x = 5", "x = 6", "x = 10"], "x = 5", "Easy"),
            ("Factorize: x² - 9", ["(x - 3)(x + 3)", "(x - 9)(x + 1)", "(x + 9)(x - 1)", "x(x - 9)"], "(x - 3)(x + 3)", "Medium"),
            ("If y = 3x and x = 4, find y.", ["7", "10", "12", "16"], "12", "Easy"),
            ("What is the slope of y = 2x + 1?", ["1", "2", "3", "-2"], "2", "Medium"),
            ("Solve: x² = 49", ["x = 7 only", "x = -7 only", "x = ±7", "x = 49"], "x = ±7", "Medium"),
        ],
        "Trigonometry": [
            ("What is sin 90°?", ["0", "1", "1/2", "√3/2"], "1", "Easy"),
            ("What is cos 0°?", ["0", "1", "-1", "1/2"], "1", "Easy"),
            ("tan θ is equal to:", ["sin θ / cos θ", "cos θ / sin θ", "1 / sin θ", "1 / cos θ"], "sin θ / cos θ", "Medium"),
            ("In a right triangle, hypotenuse is always:", ["Shortest side", "Longest side", "Equal to base", "Equal to height"], "Longest side", "Easy"),
            ("What is sin²θ + cos²θ?", ["0", "1", "tan θ", "2"], "1", "Medium"),
        ],
        "Probability": [
            ("A coin is tossed once. Probability of heads?", ["0", "1/4", "1/2", "1"], "1/2", "Easy"),
            ("A die is rolled. Probability of getting 6?", ["1/2", "1/3", "1/6", "1/12"], "1/6", "Easy"),
            ("Probability values always lie between:", ["0 and 1", "1 and 2", "-1 and 1", "0 and 100 only"], "0 and 1", "Easy"),
            ("If an event is certain, its probability is:", ["0", "0.5", "1", "2"], "1", "Medium"),
            ("Two coins are tossed. Probability of two heads?", ["1/2", "1/3", "1/4", "3/4"], "1/4", "Medium"),
        ],
        "Geometry": [
            ("Sum of angles in a triangle is:", ["90°", "180°", "270°", "360°"], "180°", "Easy"),
            ("Area of a rectangle is:", ["length + breadth", "2(length + breadth)", "length × breadth", "length / breadth"], "length × breadth", "Easy"),
            ("A square has how many equal sides?", ["2", "3", "4", "5"], "4", "Easy"),
            ("Circumference of a circle is:", ["πr²", "2πr", "πd²", "r²"], "2πr", "Medium"),
            ("Pythagoras theorem applies to:", ["Any triangle", "Right triangle", "Circle", "Square only"], "Right triangle", "Medium"),
        ],
    },
    "Physics": {
        "Motion": [
            ("SI unit of speed is:", ["m", "s", "m/s", "kg"], "m/s", "Easy"),
            ("Speed is calculated as:", ["distance/time", "time/distance", "mass × acceleration", "force/area"], "distance/time", "Easy"),
            ("Acceleration means change in:", ["Distance", "Velocity", "Mass", "Force"], "Velocity", "Medium"),
            ("An object at rest has speed:", ["0", "1", "9.8", "Cannot be measured"], "0", "Easy"),
            ("Uniform motion means:", ["Changing speed", "Constant speed", "No direction", "Circular path only"], "Constant speed", "Medium"),
        ],
        "Force and Laws of Motion": [
            ("Force is measured in:", ["Joule", "Newton", "Watt", "Pascal"], "Newton", "Easy"),
            ("Newton's first law is also called:", ["Law of inertia", "Law of energy", "Law of pressure", "Law of charge"], "Law of inertia", "Medium"),
            ("F = ma represents:", ["First law", "Second law", "Third law", "Law of gravity only"], "Second law", "Medium"),
            ("Action and reaction are:", ["Same direction", "Opposite direction", "Unrelated", "Always zero"], "Opposite direction", "Medium"),
            ("Inertia depends mainly on:", ["Mass", "Color", "Temperature", "Shape only"], "Mass", "Hard"),
        ],
        "Electricity": [
            ("SI unit of current is:", ["Volt", "Ampere", "Ohm", "Watt"], "Ampere", "Easy"),
            ("Ohm's law is:", ["V = IR", "P = VI", "F = ma", "Q = mcΔT"], "V = IR", "Medium"),
            ("A device used to measure current is:", ["Voltmeter", "Ammeter", "Thermometer", "Barometer"], "Ammeter", "Easy"),
            ("Resistance is measured in:", ["Volt", "Ampere", "Ohm", "Coulomb"], "Ohm", "Easy"),
            ("In a series circuit, current is:", ["Same everywhere", "Zero everywhere", "Different in each component", "Only in one branch"], "Same everywhere", "Hard"),
        ],
    },
    "Chemistry": {
        "Atomic Structure": [
            ("The center of an atom is called:", ["Electron", "Nucleus", "Shell", "Molecule"], "Nucleus", "Easy"),
            ("Protons have charge:", ["Positive", "Negative", "Neutral", "Variable"], "Positive", "Easy"),
            ("Electrons are found in:", ["Nucleus", "Shells/orbits", "Protons", "Neutrons"], "Shells/orbits", "Easy"),
            ("Atomic number equals number of:", ["Neutrons", "Protons", "Electrons + neutrons", "Molecules"], "Protons", "Medium"),
            ("Mass number equals:", ["Protons + neutrons", "Electrons only", "Protons only", "Neutrons only"], "Protons + neutrons", "Medium"),
        ],
        "Chemical Bonding": [
            ("Ionic bond forms by:", ["Sharing electrons", "Transfer of electrons", "Sharing protons", "Loss of neutrons"], "Transfer of electrons", "Medium"),
            ("Covalent bond forms by:", ["Sharing electrons", "Transfer of electrons", "Breaking atoms", "Creating neutrons"], "Sharing electrons", "Medium"),
            ("NaCl contains mainly:", ["Ionic bond", "Covalent bond", "Metallic bond", "Hydrogen bond only"], "Ionic bond", "Easy"),
            ("A molecule of water is:", ["H₂O", "CO₂", "NaCl", "O₂"], "H₂O", "Easy"),
            ("Valence electrons are electrons in the:", ["Nucleus", "Outermost shell", "Innermost shell", "Neutron cloud"], "Outermost shell", "Hard"),
        ],
        "Acids and Bases": [
            ("Acids turn blue litmus:", ["Red", "Green", "Blue", "Yellow"], "Red", "Easy"),
            ("Bases turn red litmus:", ["Red", "Blue", "Green", "Black"], "Blue", "Easy"),
            ("pH less than 7 indicates:", ["Acid", "Base", "Neutral", "Salt only"], "Acid", "Medium"),
            ("Neutral solution has pH:", ["0", "7", "10", "14"], "7", "Easy"),
            ("HCl is an example of:", ["Acid", "Base", "Salt", "Metal"], "Acid", "Medium"),
        ],
    },
}


def seed_database(force: bool = False) -> bool:
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

    for subject, topics in SAMPLE_DATA.items():
        upsert_subject(subject)
        for topic, questions in topics.items():
            upsert_topic(subject, topic)
            for question_text, options, correct_answer, difficulty in questions:
                db.questions.update_one(
                    {"question": question_text, "subject": subject, "topic": topic},
                    {
                        "$set": {
                            "question": question_text,
                            "options": options,
                            "correct_answer": correct_answer,
                            "subject": subject,
                            "topic": topic,
                            "difficulty": difficulty,
                        }
                    },
                    upsert=True,
                )
    return True


if __name__ == "__main__":
    ok = seed_database(force=False)
    print("Sample data seeded successfully." if ok else "MongoDB connection missing or failed.")
