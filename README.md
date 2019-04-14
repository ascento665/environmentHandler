# identityRecognition

### How to use
Upload the deployment package to the lambda server using
```
make deploy
```

Clean the file using
```
make clean
```

### Toggling events from the app
Using the apps UI one can toggle different events:
`leaving home`: make the alarm active, such that it invokes when an intruder want's to enter the building
`toggle dance mode`: enlighten the environment with flashing lights for the ultimate dance battle
`toggle romantic mode`: a romantic mode for lonely hours together as two

### Toggling events from the command line
Call the following commands from the command line.

simulate bad guy has entered
```
aws lambda invoke --function-name environmentHandler --payload '{"event": "bad_guy_entering"}' foo.txt
```

simulate good guy has entered
```
aws lambda invoke --function-name environmentHandler --payload '{"event": "good_guy_entering"}' foo.txt

```

leave house
```
aws lambda invoke --function-name environmentHandler --payload '{"event": "leaving_house"}' foo.txt

```

toggle dance mode
```
aws lambda invoke --function-name environmentHandler --payload '{"event": "requesting_dance_mode"}' foo.txt

```

toggle romantic mode
```
aws lambda invoke --function-name environmentHandler --payload '{"event": "requesting_romantic_mode"}' foo.txt

```

If an intruder was detected, the owner has 20 seconds to override a invocation of the alarm. For this call the following command.
```
aws lambda invoke --function-name overrideFunction --payload '{"event": "good_guy_entering"}' foo.txt

```
