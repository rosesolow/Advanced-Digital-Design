import simpleaudio as sa
import numpy as np
import cv2

internal_cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
notes = [440,493,523,587,659,698]


def create_note(freq=466):

    # get timesteps for each sample, T is note duration in seconds
    sample_rate = 44100
    T = .2
    t = np.linspace(0, T, int(T*sample_rate), False)

    # generate sine wave notes
    note = np.sin(freq * t * 2 * np.pi)
    return note


def play(keys=[]):
    # concatenate notes
    audio = np.hstack(keys)
    # normalize to 16-bit range
    audio = audio*32767 / np.max(np.abs(audio))
    # convert to 16-bit data
    audio = audio.astype(np.int16)

    # start playback
    sample_rate = 44100
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

    # wait for playback to finish before exiting
    #play_obj.wait_done()


def view_internal_camera():
    while True:
        # capture frame, convert to gray, show frame
        ret, image = internal_cam.read()
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imshow('Imagetest', image)
        # wait for 50ms or keystroke
        k = cv2.waitKey(20)
        # if keystroke closes window then break loop
        if k != -1:
            internal_cam.release()
            cv2.destroyAllWindows()
            break


if __name__=='__main__':
    while True:
        # capture frame, convert to gray, show frame
        ret, image = internal_cam.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # image.shape = (480,640,3)
        keys = []
        sound = []
        for i in range(6):
            cv2.circle(image, (70+100*i, 240), 20, (0, 0, 0), 2)
            avg = [np.mean(image[230:250, 70+100*i-10:70+100*i+10, 0]),
                   np.mean(image[230:250, 70+100*i-10:70+100*i+10, 1]),
                   np.mean(image[230:250, 70+100*i-10:70+100*i+10, 2])]

            print(f'circle {i}: {avg[0]}')
            if avg[0] < 70:
                sound.append(i)
                note = create_note(freq=notes[i])
                keys.append(note)
        if keys:
            print(sound)
            play(keys=keys)
        cv2.imshow('Light Harp', image)

        # wait or keystroke
        k = cv2.waitKey(20)
        # if keystroke closes window then break loop
        if k != -1:
            internal_cam.release()
            cv2.destroyAllWindows()
            break
