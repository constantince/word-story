from words import words2, words

def find_words_in_text(text, word_list):
    words = text.lower().split()
    found_words = [word for word in word_list if word.lower() in words]
    
    return found_words
    

def remove_words_in_text(text, word_list):
    words = text.lower().split()
    remaining_words = [word for word in word_list if word.lower() not in words]
    
    return remaining_words


t = """Once upon a time, in the distant past of Ancient Greece, there was a bustling pantheon of gods and goddesses who held power over the world. At the center of this pantheon was the mighty Zeus, the ruler of the gods, who sat atop Mount Olympus and oversaw all with a terrific hand. But Zeus was not the only god in this realm; many other gods and goddesses had their own power and influence, from Poseidon, the god of the seas, to Ares, the god of war. Together, these gods and goddesses formed the ballpark of power in Ancient Greece, and their stories and adventures still shape our world today. \n\nZeus had been entrusted with the power to rule over the gods, but as time went on, other gods and goddesses began to challenge his authority. Athena, the goddess of wisdom, used her cunning to outsmart Zeus while Hercules, the legendary hero of Ancient Greece, stood as a champion of the people, defying the gods and goddesses in order to protect the innocent. \n\nThe conflict between Zeus and the other gods and goddesses became an ever-present one, as each sought to gain control and influence over the lands. Ares, the god of war, led the charge against Zeus, attempting to overthrow his rule with force, while Poseidon, the god of the sea, sought to unblock the paths of power with the moisture of the waves. It seemed that the gods and goddesses of Ancient Greece were determined to challenge Zeus, and their efforts to do so made for an utter understatement of the enormity of the struggle."""

found_words = remove_words_in_text(t, words)
print("The following words from the list are present in the text:", found_words)