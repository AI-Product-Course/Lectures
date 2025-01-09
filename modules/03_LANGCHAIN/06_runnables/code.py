import math
from langchain_core.runnables import RunnableLambda, RunnableSequence, RunnableParallel, RunnablePassthrough

# RunnableLambda
square_runnable = RunnableLambda(lambda x: x ** 2)
result = square_runnable.invoke(10)
print("square_runnable", result)

# RunnableSequence
add_10_runnable = RunnableLambda(lambda x: x + 10)
log_runnable = RunnableLambda(lambda x: math.log(x))

pipeline = RunnableSequence(square_runnable, add_10_runnable, log_runnable)
result = pipeline.invoke(10)
print("sequence_runnable", result)

# RunnableParallel
pipeline = RunnableParallel(square_result=square_runnable, add_10_result=add_10_runnable)
result = pipeline.invoke(2)
print("parallel_runnable", result)

# RunnablePassthrough
alternative_square_runnable = RunnableLambda(lambda data: data["initial_value"] ** 2)
pipeline = RunnablePassthrough.assign(square_result=alternative_square_runnable)
res = pipeline.invoke({"initial_value": 2})
print("passthrough_runnable", res)
