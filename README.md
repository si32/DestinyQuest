# Destiny Quest Hero List
#### Video Demo:  <https://youtu.be/A9OcwPh5mfA>
#### Description: Python project to help people play to DestinyQuest game-book series

## General information
This Application has to hepl people to play in Destiny Quest gamebook series.

If you're unfamiliar with gamebooks, these are books broken into numbered paragraphs. Sometimes a hero, that is, you
offer to make a choice. For example go right or left. Depending on your choice, you go
to a specific paragraph number. Sometimes during the adventureyou meet enemies and have to fight them.
Sometimes get tested. For example, a strength test to break a lock or agiliti test to climb a cliff.

Tests and fights take place on dice, taking into account the parameters that you have.

During the adventure, you can find things (swords, rings, helmets and etc.) that will change your agililty, brawn, magic or armour parameters. And of course you have some health points.

All this is taken into account in my program.

### How to ...
You can choose the name of your hero, his path and career by clicking the name label.

You can pass tests by clicking on a specific parameter you want to test.

You can fight with an enemy by writing down its characteristics in the enemy field.
The fight takes place in two stages. First, you will test your agility and the agility of the enemy.
Whoever has a higher agility value will attack by striking with your brawn or magic power. It depends on which parametr is higher (You are ⚔️warrior or 🧙mage)

In equioment section (**"Equipment"** button) you can see what equipment you are currently wearing.
You can put the item in your backpack (using **"In Backpack"** button) or throw it away (using **"Thow away"** button) if there is no space in backpack (backpack has just 5 cells).

If you find a new item you can wear it on different place depends on type of item. Swords in hands, helmets on head, boots on feet and etc... Choose the right place, write down name, type and parameters of item and click "Put on/Apply" button. When you wear new item - it will change your parameters.

Also there are some items you cann't wear on and can put it in backpack.
For example? poition. You can drink some poition that temporary change your parameters (add health point in a battle or increase some parameter to pass the test).

You can keep track of the money you have in you money pouch.

### Loading and saving the character.
You can use menubar to save your progress and continue the game later by loading it.
Files save in json forma in folder ./SaveData in current folder.

## About application
Application is written in python languages using Tkinter library.

I use OOP to structure the code. It helps use many functions without worrying about passing the necessary parameters of the window object to them.

I use a separete class for player to save all characteristics and parameters in one object. In general use player object as a data base. Class player is licated in separete file (player.py) where I also keep data for a new hero and function for serialization object player in json format to save hero.

For each child window I use separete class also. It helps to structer the code.
