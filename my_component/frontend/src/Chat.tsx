import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"

interface State {
  image: string
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class Chat extends StreamlitComponentBase<State> {
  public state : State = { image: this.props.args["image"] }

  componentDidMount() {
    document.addEventListener("fullscreenchange", this.onFullScreenChange);
  }

  componentWillUnmount() {
    document.removeEventListener("fullscreenchange", this.onFullScreenChange);
  }

  handleImageClick = (event: React.MouseEvent<HTMLImageElement, MouseEvent>) => {
    const element = event.currentTarget;
    if (element.requestFullscreen) {
      element.requestFullscreen();
    } else if ((element as any).webkitRequestFullscreen) { // Safari
      (element as any).webkitRequestFullscreen();
    } else if ((element as any).msRequestFullscreen) { // IE11
      (element as any).msRequestFullscreen();
    }
  }

  onFullScreenChange = () => {
    if (document.fullscreenElement) {
      // Add semi-transparent background and close button when in full screen
      const fullscreenElement = document.fullscreenElement as HTMLElement;
      fullscreenElement.style.background = 'rgba(0, 0, 0, 0.5)';
      const closeButton = document.createElement('button');
      closeButton.innerText = 'Close';
      closeButton.onclick = () => document.exitFullscreen();
      document.fullscreenElement.appendChild(closeButton);
    }
  }

  public render = (): ReactNode => {
    // Show a button and some text.
    // When the button is clicked, we'll increment our "numClicks" state
    // variable, and send its new value back to Streamlit, where it'll
    // be available to the Python program.
    return (
      <>
        <div className="">
          <img onClick={this.handleImageClick} src={this.state.image} alt="Thomas More Logo" width="150px" />
        </div>
      </>
    )
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(Chat)
