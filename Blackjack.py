import random

def main():
    # All of this is to set up 'deck' which we can now pass into 'set_up_shoe' to get a shuffled shoe with a cut card in it
    class Card:
        def __init__(self, suit, rank):
            self.suit = suit
            self.rank = rank

        def __repr__(self):
            return f"{self.rank} of {self.suit}"

    deck = []
    suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
    ranks = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']


    for i in range(8):
        for suit in suits:
            for rank in ranks:
                deck.append(Card(suit, rank))
    # Now that we have a shoe, we need to deal cards to both the player and dealer. We also need to give the user both their score and the dealer's score
    
    

    


def set_up_shoe(shoe):
    random.shuffle(shoe)
#The cut card needs to go somewhere from the start of the deck to the first third (because pop takes from the end)
    cut_upper_bound = int(len(shoe) * 0.3) 
    cut_lower_bound = int(len(shoe) * 0.25) 
    cut_pos = random.randint(cut_lower_bound, cut_upper_bound)
    
    shoe.insert(cut_pos, 'Cut Card')
    return shoe


         


if __name__ == '__main__':
        main()

