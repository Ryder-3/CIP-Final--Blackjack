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


    # Betting logic
    player_balance = input("Choose your starting balance: (out of 50, 100, or 150) ")
    while player_balance not in ['50', '100', '150']:
        player_balance = input("Invalid choice. Please choose your starting balance: (out of 50, 100, or 150) ")
    player_balance = int(player_balance)


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
    blackjack = False
    won_1 = False
    won_2 = False
    push = False
    print("Welcome to Blackjack!")
    seed = random.randint(0,2**32 - 1)
    random.seed(seed)
    print("For testing, the seed of this run is", seed, ".")
    
    while playing == True:


        #Betting
        bet = input(f"Your current balance is {player_balance}. How much would you like to bet? ")
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
                dealer_hand.append(card)
            
            card, temp_pass_cut = deal_card(shoe)
            if temp_pass_cut == True:
                passed_cut_card = True
            if card:
                player_hand.append(card)

        #checking if the player can split
        if player_hand[0].rank == player_hand[1].rank:
            split_choice = input(f"You have a pair of {player_hand[0].rank}'s Do you want to split? (yes/no) ")
            if split_choice.lower() == 'yes':
                # Split the hand into two hands
                player_hand_1 = [player_hand[0]]
                card, temp_pass_cut = deal_card(shoe)
                if temp_pass_cut == True:
                    passed_cut_card = True
                if card:
                    player_hand_1.append(card)


                player_hand_2 = [player_hand[1]]
                card, temp_pass_cut = deal_card(shoe)
                if temp_pass_cut == True:
                    passed_cut_card = True
                if card:
                    player_hand_2.append(card)
                    
                player_score_1 = calculate_player_score(player_hand_1)
                player_score_2 = calculate_player_score(player_hand_2)

            else:
                player_hand_1 = player_hand
                player_score_1 = calculate_player_score(player_hand_1)
        else:
            split_choice = 'no'
        
        if split_choice.lower() != 'yes':
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
        else:
            print(f"Your first hand: {player_hand_1} | Your score: {player_score_1}")
            player_stand_1 = False
            #player gameplay for first hand
            while player_stand_1 == False:
                if player_score_1 > 21:
                    print("You busted! Dealer wins.")
                    player_stand_1 = True
                    lost = True
                    break
                elif player_score_1 == 21:
                    print("Blackjack! You win!")
                    player_stand_1 = True
                    won_1 = True
                    break
                player_choice = input("Do you want to Hit or Stand? ")
                if player_choice.lower() == 'hit':
                    card, temp_pass_cut = deal_card(shoe)
                    if temp_pass_cut == True:
                        passed_cut_card = True
                    if card:
                        player_hand_1.append(card)
                        player_score_1 = calculate_player_score(player_hand_1)
                        print(f"Your hand: {player_hand_1} | Your score: {player_score_1}")
                elif player_choice.lower() == 'stand':
                    player_stand_1 = True
            print(f"Your second hand: {player_hand_2} | Your score: {player_score_2}")
            player_stand_2 = False
            #player gameplay for second hand
            while player_stand_2 == False:
                if player_score_2 > 21:
                    print("You busted! Dealer wins.")
                    player_stand_2 = True
                    lost = True
                    break
                elif player_score_2 == 21:
                    print("Blackjack! You win!")
                    player_stand_2 = True
                    won_2 = True
                    break
                player_choice = input("Do you want to Hit or Stand? ")
                if player_choice.lower() == 'hit':
                    card, temp_pass_cut = deal_card(shoe)
                    if temp_pass_cut == True:
                        passed_cut_card = True
                    if card:
                        player_hand_2.append(card)
                        player_score_2 = calculate_player_score(player_hand_2)
                        print(f"Your hand: {player_hand_2} | Your score: {player_score_2}")
                elif player_choice.lower() == 'stand':
                    player_stand_2 = True
        

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
        

        #Winning logic (splits not included)
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
        won_1 = False
        won_2 = False

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