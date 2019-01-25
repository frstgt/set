# stevtb

## description

"stevtb" is "State Event Table".
You can make some state transition tables with Python, and run it.

## install/uninstall

  You can install stevtb to ~/bin and uninstall it.  
  > make install  
  > make uninstall

## run

  > stevtb

## usage

  - You can append tables with '+' button
        and remove with '-' button
        and edit with 'E' button.
  - You can reorder tables with drag&drop.

  - You can append states with '+' button
        and remove with '-' button
        and edit with 'E' button.
  - You cannot reorder states. # sorry

  - You can append tables with table's '+' button
        and remove with '-' button
        and edit with 'E' button.
  - You cannot reorder events. # sorry

  - Programs start from 'start' state of 'main' table
         and end at 'end' state.
  - A table need 'start' and 'end' state.

  - States can have Python statement.
  - Events need Python expression as condition.

  - You can call another table
    with a state has '# call (table name)' as code.

## bug

  - You cannot stop program with 'Stop' button.
    You need kill the process under such situation.

