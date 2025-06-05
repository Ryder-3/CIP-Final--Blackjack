import random
def main():
    # All of this is to set up 'deck' which we can now pass into 'set_up_shoe' to get a shuffled shoe with a cut card in it
    class Card:
        def __init__(self, suit, rank):
            self.suit = suit
            self.rank = rank

        @property
        def value(self):
            if self.rank in ['J', 'Q', 'K']:
                return 10
            elif self.rank == 'A':
                return 11
            else:
                return int(self.rank)

        def __repr__(self):
            return f"{self.rank} of {self.suit}"
    
    
    
    class Hand:
        def __init__(self):
            self.cards = []
            self.lost = False
            self.won = False
            self.blackjack = False
            self.push = False
            self.bet = False
    

    deck = []
    suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
    ranks = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']

    for i in range(8):
        for suit in suits:
            for rank in ranks:
                deck.append(Card(suit, rank))
    shoe = set_up_shoe(deck)
    # Now that we have a shoe, we need to deal cards to both the player and dealer. We also need to give the user both their score and the dealer's score
    



    player_score = 0
    player_hands = [Hand()]

    dealer_score = 0
    dealer_hand = Hand()

    playing = True
    passed_cut_card = False

    lost = False
    won = False
    blackjack = False
    bet = 0
    push = False
    print("Welcome to Blackjack!")
   


        #setting up the round
    for i in range(2):
        card, temp_pass_cut = deal_card(shoe)
        if temp_pass_cut == True:
            passed_cut_card = True
        if card:
            player_hands[0].cards.append(card)
        card, temp_pass_cut = deal_card(shoe)
        if temp_pass_cut == True:
            passed_cut_card = True
        if card:
            dealer_hand.cards.append(card)
    
    for i, hand in enumerate(player_hands):
        if hand.cards[0].rank == hand.cards[1].rank:
            split_choice = input(f"You have a pair of {hand.cards[0].rank}, would you like to split them? (yes/no)")
            if split_choice.lower() == 'yes':
                split_card = hand.cards.pop()
                player_hands.append(Hand())
                


    








def deal_card(shoe):
    if shoe[-1] != 'Cut Card':
        return shoe.pop(), False
    else:
        shoe.pop()
        print("Cut card has been reached. This is the last hand of the shoe.")
        return shoe.pop(), True

def set_up_shoe(set_shoe):
    random.shuffle(set_shoe)
#The cut card needs to go somewhere from the start of the deck to the first third (because pop takes from the end)
    cut_upper_bound = int(len(set_shoe) * 0.3) 
    cut_lower_bound = int(len(set_shoe) * 0.25) 
    cut_pos = random.randint(cut_lower_bound, cut_upper_bound)
    
    set_shoe.insert(cut_pos, 'Cut Card')
    return set_shoe

if __name__ == '__main__':
    main()