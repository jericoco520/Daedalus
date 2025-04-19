### TO-DO
- Try adding a start of file byte to tell nrf when it found the correct start transmission 
  - --> keep a list of 32 byte chunks size 3
  - Check if that list has 3 chunks we are looking for
    - Using 4 bytes in chunk to identify it is a file chunk
  - If 3 chunks identified start reading rest

- Try instead just using 4 bytes as identifiers of correct chunk to write to output file?

### Problems
- Receiving phantom bytes on receiver
- NRF configurations are not consistent
- NRF sometimes not identified