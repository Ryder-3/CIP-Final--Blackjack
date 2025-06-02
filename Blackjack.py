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
    player_hand = []

    dealer_score = 0
    dealer_hand = []

    playing = True
    passed_cut_card = False

    lost = False
    won = False

    while playing == True:

        #setting up the round
        for i in range(2):
            card, temp_pass_cut = deal_card(shoe)
            if temp_pass_cut == True:
                passed_cut_card = True
            if card:
                dealer_hand.append(card)
            
            card, temp_pass_cut = deal_card(shoe)
            if temp_pass_cut == True:
                passed_cut_card = True
            if card:
                player_hand.append(card)

        #update the player score and dealer score
        player_score = calculate_player_score(player_hand)
        dealer_score = calculate_dealer_score(dealer_hand)



        print("Welcome to Blackjack!")
        print("The dealer is showing: ", dealer_hand[0])

        print(f"Your hand: {player_hand} | Your score: {player_score}")


        #giving the player their hand and choices
        player_stand = False
        #player gameplay
        while player_stand == False:
            if player_score > 21:
                print("You busted! Dealer wins.")
                player_stand = True
                lost = True
                break
            elif player_score == 21:
                print("Blackjack! You win!")
                player_stand = True
                won = True
                break
            player_choice = input("Do you want to Hit or Stand? ")
            if player_choice.lower() == 'hit':
                card, temp_pass_cut = deal_card(shoe)
                if temp_pass_cut == True:
                    passed_cut_card = True
                if card:
                    player_hand.append(card)
                    player_score = calculate_player_score(player_hand)
                    print(f"Your hand: {player_hand} | Your score: {player_score}")
            elif player_choice.lower() == 'stand':
                player_stand = True
        

        #dealer gameplay

        if lost == False and won == False:
            while dealer_score < 17:
                card, temp_pass_cut = deal_card(shoe)
                if temp_pass_cut == True:
                    passed_cut_card = True
                if card:
                    dealer_hand.append(card)
                    dealer_score = calculate_dealer_score(dealer_hand)
                    print(f"Dealer's hand: {dealer_hand} | Dealer's score: {dealer_score}")
                    input("Press Enter to continue...")
            print(f"Dealer's final hand: {dealer_hand} | Dealer's final score: {dealer_score}")
        
            #determine the winner
            if dealer_score > 21:
                print("Dealer busted! You win!")
            elif player_score > dealer_score:
                print("You win!")
            elif player_score < dealer_score:
                print("Dealer wins!")
            else:
                print("Push!")
        elif lost:
            print(f"You lost this round. Dealer's final hand: {dealer_hand}")
        elif won:
            print(f"You won this round! Dealer's final hand: {dealer_hand}")





        # Reset hands and scores for the next round
        player_hand = []
        dealer_hand = []
        player_score = 0
        dealer_score = 0
        lost = False
        
        

        
        # Reset the shoe if the cut card has been passed
        if passed_cut_card:
            shoe = set_up_shoe(deck)
            passed_cut_card = False
            print("The shoe has been reshuffled.")
        
        # Ask if the player wants to play again
        play_again = input("Do you want to play again? (yes/no) ")
        if play_again.lower() == 'no':
            playing = False
            print("Thanks for playing!")


def calculate_player_score(player_hand):
    player_score = 0
    for card in player_hand:
        player_score += card.value
    return player_score

def calculate_dealer_score(dealer_hand):
    dealer_score = 0
    for card in dealer_hand:
        dealer_score += card.value
    return dealer_score

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

