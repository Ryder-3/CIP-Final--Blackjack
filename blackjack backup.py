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
            self.bet = 0
            self.playing = True
        @property
        def score(self):
            hand_score = 0
            aces = 0
            for card in self.cards:
                hand_score += card.value
                if card.rank == 'A':
                    aces += 1
            while hand_score > 21 and aces:
                hand_score -= 10
                aces -= 1
            return hand_score
        

    

    deck = []
    suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
    ranks = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']

    for i in range(8):
        for suit in suits:
            for rank in ranks:
                deck.append(Card(suit, rank))




    shoe = set_up_shoe(deck)
    # Now that we have a shoe, we need to deal cards to both the player and dealer. We also need to give the user both their score and the dealer's score
    



    player_hands = [Hand()]
    dealer_hand = Hand()

    passed_cut_card = False
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
    


    i = 0
    while i < len(player_hands):
        hand = player_hands[i]
        if len(hand.cards) == 2 and hand.cards[0].rank == hand.cards[1].rank:
            split_choice = input(f"You have a pair of {hand.cards[0].rank}, would you like to split them? (yes/no) ")
            if split_choice.lower() == 'yes':
                # Splitting the hand
                split_card = hand.cards.pop()
                new_hand = Hand()
                new_hand.cards.append(split_card)
                player_hands.append(new_hand)

                # Add another card to both hands
                card, temp_pass_cut = deal_card(shoe)
                if temp_pass_cut == True:
                    passed_cut_card = True
                if card:
                   hand.cards.append(card)
                card, temp_pass_cut = deal_card(shoe)
                if temp_pass_cut == True:
                    passed_cut_card = True
                if card:
                    new_hand.cards.append(card)
        for hands in player_hands:
            print(hands.cards)
        i += 1

    for hand in player_hands:
        # Check if there's a blackjack
        if hand.score == 21:
            hand.blackjack == True
            hand.playing == False

        
        
        # If there isn't a blackjack, then they play

        # they can only double the first time
        print(f"Your hand: {hand.cards}")
        print(f"Your score: {hand.score}")
        player_choice = input("Would you like to Hit, Stand, or Double? ")
        while player_choice.lower() not in ['hit', 'stand', 'double']:
            player_choice = input("Invalid choice. Please choose if you want to hit, stand, or double. ")
        if player_choice.lower() == 'double':
            card, temp_pass_cut = deal_card(shoe)
            if temp_pass_cut == True:
                passed_cut_card = True
            if card:
                hand.cards.append(card)
            if hand.score > 21:
                hand.lost = True
            if hand.score == 21:
                hand.blackjack = True
            hand.bet = hand.bet * 2
            hand.playing = False
        elif player_choice.lower() == 'hit':
            card, temp_pass_cut = deal_card(shoe)
            if temp_pass_cut == True:
                passed_cut_card = True
            if card:
                hand.cards.append(card)
            if hand.score > 21:
                hand.lost = True
            if hand.score == 21:
                hand.blackjack = True
        else:
            hand.playing = False
            
            

        while hand.playing == True:
            pass



                


    








def deal_card(shoe):
    if shoe[-1] != 'Cut Card':
        return shoe.pop(), False
    else:
        shoe.pop()
        print("Cut card has been reached. This is the last hand of the shoe.")
        return shoe.pop(), True

def set_up_shoe(set_shoe):
    #random.shuffle(set_shoe)
#The cut card needs to go somewhere from the start of the deck to the first third (because pop takes from the end)
    cut_upper_bound = int(len(set_shoe) * 0.3) 
    cut_lower_bound = int(len(set_shoe) * 0.25) 
    cut_pos = random.randint(cut_lower_bound, cut_upper_bound)
    
    set_shoe.insert(cut_pos, 'Cut Card')
    return set_shoe

if __name__ == '__main__':
    main()