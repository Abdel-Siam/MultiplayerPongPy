# Dynamic Pong
## Considerations:
### 1 - Signals
Updates would need to include :

1. New Velocities (Server)
2. Collisions (Server? Client? Both?)
3. User movement (Client -> Server)
4. Score updates (Server -> Clients)

---

PONG RULES
1. First to 11 wins
2. Alternating ball positioning (left then right then left then right [...])[^1]
3. Ball starts at a random position on the midpoint of the y axis
4. Ball goes down (can be changed)


[^1]: This can be changed to be coin flip based.