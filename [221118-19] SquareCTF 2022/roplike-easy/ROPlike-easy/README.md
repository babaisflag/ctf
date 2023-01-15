# ROPlike

## Point Value
250

## Challenge Description
I've been working on a new <a href='/static/files/ROPlike-easy/roplike'>roguelite idea</a>, I think its got great potential.

## Description
This is a pwnable that gives you full stack control of 256 bytes and returns to the top of that buffer, with all memory protections enabled. The binary is structured like a round-based roguelite where you have the ability to purchase rop gadgets from a randomized store, where purchasing gadgets will map them into memory at a static and predictable address. The idea is that players will use the rop gadgets to either cheat the game to give them more currency than is actually possible in order to buy the syscall gadget, or otherwise just leak enough information to reuse the binary functions to print out the flag.

## Deployment
players need the roplike binary, otherwise this should be deployed like a typical pwnable with the dockerfile in this directory.