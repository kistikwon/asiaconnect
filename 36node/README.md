score 
eq : total = pretotal + loss + throughput + delay

pretotal mean previously selected node score
in first total it does not appled 

loss  = 20 - Loss_value * Loss_weight
delay = 40 - delay_value * delay_weight
throughput = 40 * throughput_value * throughput_weight

example.
Node1 = A1 -> A2
        A1 -> A3
        A1 -> A4
        A1 -> A5
        A1 -> A6
        
highst [A1 -> A6] score A6 will select node

Node6 = A6 -> A2
        A6 -> A3
        A6 -> A4
        A6 -> A5
        
sum Node1 score and Node6 score
[A1 -> A2] + [A6 -> A2]
[A1 -> A3] + [A6 -> A3]
[A1 -> A4] + [A6 -> A4]
[A1 -> A5] + [A6 -> A5]

and highst [A1 -> A4] + [A6 -> A4] score A4 will next select node


      
