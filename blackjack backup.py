import random
def main():
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
            self.done = False
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
    print()
    while True:
        chips = input("Choose your starting value: 50, 100, or 150 ")
        while chips not in ['50', '100', '150']:
            chips = input('Invalid choice, please choose 50, 100, or 150 ')
        chips = int(chips)

        player_hands[0].bet = input(f"You have {chips} chips, how much would you like to bet?")
        while int(player_hands[0].bet) > chips:
            print(f"You can't bet {player_hands[0].bet} chips, you only have {chips} chips.")
            player_hands[0].bet = input(f"You have {chips} chips, how much would you like to bet?")
        player_hands[0].bet = int(player_hands[0].bet)

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
                    new_hand.bet = player_hands[i].bet
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
                hand.blackjack = True
                hand.playing = False

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

            # This is for every hand after the first (the only real difference is that they can't double anymore)
            while hand.playing == True:
                print(f"Your hand: {hand.cards}")
                print(f"The dealer's card: {dealer_hand.cards[0]}")
                print(f"Your score: {hand.score}")
                player_choice = input("Would you like to Hit or Stand? ")
                while player_choice.lower() not in ['hit', 'stand']:
                    player_choice = input("Invalid choice. Please choose if you want to hit or stand. ")
                if player_choice.lower() == 'hit':
                    card, temp_pass_cut = deal_card(shoe)
                    if temp_pass_cut == True:
                        passed_cut_card = True
                    if card:
                        hand.cards.append(card)
                    if hand.score > 21:
                        hand.lost = True
                        hand.playing = False
                    if hand.score == 21:
                        hand.blackjack = True
                        hand.playing = False
                else:
                    hand.playing = False  

            # Now that the player has played their hand we check to see if they lost or hit a blackjack
            if hand.lost == True:
                print("You Busted!")
                print(f"Your final score was {hand.score}")
                chips -= hand.bet
                hand.done = True
            elif hand.blackjack == True:
                print("Blackjack! You win 1.5x your bet!")
                print("Your final score was 21! Good job!")
                chips += hand.bet * 1.5
                hand.done = True
        # We now need to leave the for loop so the dealer can take their turn. We will go back into another one later to compare all of the scores
        if not all(hand.done for hand in player_hands):
            print(f"Dealer's score: {dealer_hand.score}")
            input("Press enter to continue")
            while dealer_hand.score < 17:
                card, temp_pass_cut = deal_card(shoe)
                if temp_pass_cut == True:
                    passed_cut_card = True
                if card:
                    dealer_hand.cards.append(card)
                print(f"Dealer's score: {dealer_hand.score}")
                input("Press enter to continue")
            # These just set each hand to winning or not
            if dealer_hand.score > 21:
                for hand in player_hands:
                    if hand.lost == False:
                        hand.won = True
            else:
                for hand in player_hands:
                    if hand.lost == False and hand.blackjack == False:
                        if hand.score > dealer_hand.score:
                            hand.won = True
                        elif hand.score < dealer_hand.score:
                            hand.lost = True
        # Now we just need to print whether or not each hand won, and adjust the Player's chip amounts.
        i = 1
        for hand in player_hands:
            print(f"We're looking at hand number {i}.")
            if hand.won == True:
                print(f"You won this hand! Your {hand.score} beat the dealer's {dealer_hand.score}")
                chips += hand.bet
            elif hand.lost == True and hand.done == False:
                print(f"You lost this hand. The dealer's {dealer_hand.score} beat your {hand.score}")
                chips -= hand.bet
            elif hand.score == dealer_hand.score:
                print(f"Its a tie! You and the dealer both had a score of {hand.score}.")
            i += 1
        print(f"You now have {chips} chips.")
        play_again = input("Would you like to play again? (yes/no) ")
        while play_again.lower() not in ['yes', 'no']:
            play_again = input("Invalid choice, please chose yes or no")

        # Resetting everything
        player_hands = [Hand()]
        dealer_hand = Hand()
        
        if play_again.lower() == 'no':
            break

        if passed_cut_card == True:
            print("The cut card was passed this round. The shoe will now be reshuffled")
            shoe = set_up_shoe(deck)
            passed_cut_card = False

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