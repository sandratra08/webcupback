from project.router.user.user import router as userRouter
from project.router.nlp.nlp import router as nlpRouter

params = [
    [
        userRouter,
        "/auth"
    ],
    [
        nlpRouter,
        "/dreams"
    ]
]
