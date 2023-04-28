ft_otp

In this project, the aim is to implement a TOTP (Time-based One-Time Password)
system, which will be capable of generating ephemeral passwords from a master key.
It will be based on the RFC: https://datatracker.ietf.org/doc/html/rfc6238

Implement a program that allows you to register
an initial password, and is capable of generating a new password each time it is requested.
You can use any library that facilitates the implementation of the algorithm, as long as
they do not do the dirty work, that is, it is strictly forbidden to use any TOTP library.
Of course, you can and should make use of some library or function that allows you to
access system time
