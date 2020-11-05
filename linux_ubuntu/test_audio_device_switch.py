from ubuntu_AudioDeviceManager import AudioDeviceManager

if __name__ == "__main__":
    ## Example usage
    myAudio = AudioDeviceManager()

    try: txt = int(input("Give 0 for outputs, 1 for inputs: "))
    except ValueError:
        print('Invalid input, exiting.')
        exit()

    if 0 == txt:
        # Get current device name
        currentSink = myAudio.sinks.getCurrentSinkDevice() 
        print('Current Output: ', currentSink[0])

        # Get all sinks
        allSinks = myAudio.sinks.getSinkDescriptions()
        print('All Outputs:')
        for i in range(len(allSinks)): print(i, ':', allSinks[i])

        # Switch Device
        try: choice = int(input("Choose Output (index): "))
        except ValueError:
            print('Invalid input, exiting.')
            exit()
        
        if choice in range(len(allSinks)):
            myAudio.sinks.switchSinkDevice(allSinks[choice])
        else:
            print('Invalid choice.')

    elif 1 == txt:
        # Get current device name
        currentSource = myAudio.sources.getCurrentSourceDevice()
        print('Current Input: ', currentSource[0])

        # Get all sources
        allSources = myAudio.sources.getSourceDescriptions()
        print('All Inputs:')
        for i in range(len(allSources)): print(i, ':', allSources[i])

        # Switch Device
        try: choice = int(input("Choose Input (index): "))
        except ValueError:
            print('Invalid input, exiting.')
            exit()

        if choice in range(len(allSources)):
            myAudio.sources.switchSourceDevice(allSources[choice])
        else:
            print('Invalid choice.')

    else: 
        print('Invalid input, exiting.')
        exit()