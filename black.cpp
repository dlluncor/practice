#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

using namespace std;

void playBlackjack() {
  cout << "Im playing blackjack\n";
}

int main() {

  char userResp = 'y';

  while(userResp == 'y') {
    playBlackjack();
    cout << "Do you want to play again?";
    cin >> userResp;
  }
}