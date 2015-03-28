from __future__ import division
import sys
import numpy as np
import pylab as pl

class VerifyError(Exception):
    pass

def verify_user_input(prompt, passphrase):
    '''
    verify that a user inputs a specific response to a prompt
    otherwise, raise an error

    Parameters
    ----------
    prompt : str
        text to prompt the user with

    passphrase : str
        the phrase required to return true

    Returns
    -------
    pass : bool
        True if the user input matches the passphrase
        False if the input doesn't match, or if the user escapes with a keyboard interrupt

    '''

    try:
        assert raw_input(prompt) == passphrase

    except (AssertionError, KeyboardInterrupt):
        return False

    return True



def verify_im(im, text, passphrase):

    started_interactive = pl.isinteractive()

    pl.ion()
    pl.figure('Image Verification')
    pl.imshow(im)

    verified = verify_user_input(text, passphrase)

    pl.close('Image Verification')

    if not started_interactive:
        pl.ioff()

    return verified



