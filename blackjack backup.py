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
            lost = False
    

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
    player_hand = Hand()

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
   

        # Betting logic
    player_balance = input("Choose your starting balance: (out of 50, 100, or 150) ")
    while player_balance not in ['50', '100', '150']:
        player_balance = input("Invalid choice. Please choose your starting balance: (out of 50, 100, or 150) ")
    player_balance = int(player_balance)

    
    while playing == True:


        #Betting
        bet = input(f"Your current balance is {player_balance}. How much would you like to bet? ")
        while not bet.isdigit() or int(bet) <= 0 or int(bet) > player_balance:
            bet = input(f"Invalid bet. Please enter a valid amount to bet (between 1 and {player_balance}): ")
        bet = int(bet)
        while bet <= 0 or bet > player_balance:
            bet = input(f"Invalid bet. Please enter a valid amount to bet (between 1 and {player_balance}): ")
            bet = int(bet)
        #Betting for split hands is not done at all

        #setting up the round
        for i in range(2):
            card, temp_pass_cut = deal_card(shoe)
            if temp_pass_cut == True:
                passed_cut_card = True
            if card:
                player_hand.cards.append(card)
            #Start work here


        #checking if the player can split
#TEMP CODE TEMP CODE TEMP CODE TEMP CODE TEMP CODE TEMP CODE TEMP CODE TEMP CODE TEMP CODE
        #player_hand = [Card('Spade', 'K'), Card('Heart', 'K')]



    
        player_score = calculate_player_score(player_hand)
        dealer_score = calculate_dealer_score(dealer_hand)


        if player_score == 21:
            blackjack = True
        else:
    
            print("The dealer is showing: ", dealer_hand[0])

            print(f"Your hand: {player_hand} | Your score: {player_score}")

            #giving the player their hand and choices
            player_stand = False

            #player gameplay
            while player_stand == False:
                if player_score > 21:
                    player_stand = True
                    lost = True
                    break
                elif player_score == 21:
                    player_stand = True
                    blackjack = True
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
        if lost == False and won == False and blackjack == False:
            print("Dealer's turn.")
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
            input("Press Enter to continue...")
    

        #Winning logic
        if lost == False and won == False and blackjack == False:
            if dealer_score > 21:
                won = True
            elif dealer_score == player_score:
                push = True
            elif dealer_score > player_score:
                lost = True
            else:
                won = True
    #Paying out bets
        if blackjack:
            player_balance += int(bet * 1.5)
            print(f"Your hand: {player_hand} | Your score: {player_score}")
            print(f"You won {int(bet * 1.5)}! Your new balance is {player_balance}.")
        elif won:
            player_balance += bet
            print(f"You won {bet}! Your new balance is {player_balance}.")
        elif lost:
            player_balance -= bet
            print(f"You lost {bet}. Your new balance is {player_balance}.")
        elif push:
            print(f"It's a push! Your balance remains {player_balance}.")


        # Reset hands and scores for the next round
        player_hand = []
        dealer_hand = []
        player_score = 0
        dealer_score = 0
        lost = False
        won = False
        push = False
        blackjack = False

        # Reset the shoe if the cut card has been passed
        if passed_cut_card:
            shoe = set_up_shoe(deck)
            passed_cut_card = False
            print("The shoe has been reshuffled.")
        
        # Ask if the player wants to play again
        if player_balance <= 0:
            print("You have run out of money! Thanks for playing!")
            break
        play_again = input("Do you want to play again? (yes/no) ")
        if play_again.lower() == 'no':
            playing = False
            print(f"Your final balance is {player_balance}.")
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