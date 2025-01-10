import chainlit as cl
import matplotlib.pyplot as plt


def get_plot() -> plt.Figure:
    import numpy as np
    fig, ax = plt.subplots()
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)
    ax.plot(x, y)
    ax.set_title('Синусоида')
    return fig


@cl.on_message
async def handle_message(message: cl.Message):
    parrot_image = cl.Image(path="./parrot.jpg", name="Parrot Image", size="small")
    parrot_code = cl.File(path="./parrot.py", name="Parrot Code")
    parrot_pdf = cl.Pdf(path="./parrot.pdf", page=1, name="Parrot Article")
    parrot_pplot = cl.Pyplot(name="Parrot Plot", figure=get_plot(), display="inline")
    msg = cl.Message(
        content=f"Your message: {message.content}",
        elements=[
            parrot_image, parrot_code,  parrot_pdf, parrot_pplot
        ]
    )
    await msg.send()
