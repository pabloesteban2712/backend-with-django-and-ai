from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import User
from main.models import Article
from main.serializers import ArticleSerializer
from main.validator import ArticleValidatorForm
from django.core.paginator import Paginator
from django.conf import settings
import json
from openai import OpenAI

@csrf_exempt
def save(request):
    if request.method == "POST":

        if request.POST and request.POST.get("title", False) and request.POST.get("content", False):

            user = User.objects.get(id = request.user.id)

            form = ArticleValidatorForm(request.POST)

            if form.is_valid():

                article = Article(
                    title = request.POST['title'],
                    content = request.POST['content'],
                    user = user
                )

            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Error with the validation"
            }) 

            try:
                article.save()

                articleS = ArticleSerializer(article, many=False)

                return JsonResponse({
                    "status": "success",
                    "article": articleS.data
            }) 

            except Exception as e:
                return JsonResponse({
                    "status": "error",
                    "message": "Error saving" 
                }) 

    else:
        return JsonResponse(
            {"status": "Error",
             "message": "HTTP method is not allowed"})

@csrf_exempt
def getArticles(request):
    if request.method == "GET":
        
        itemsPerPage = 5

        try:
            allArticle = Article.objects.all()
            
            paginator = Paginator(allArticle, itemsPerPage)

            page = request.POST.get("page", 1)

            articlesPerPage = paginator.page(page)

            pageObj = paginator.get_page(page)

            articles = ArticleSerializer(articlesPerPage, many=True)

            return JsonResponse({
                "status": "success",
                "articles": articles.data,
                "itemsPerPage": itemsPerPage,
                "pages": pageObj.paginator.num_pages,
                "totalArticles": len(allArticle)
            })

        except Exception as e:

            return JsonResponse({
                "status": "Success",
                "action": "getArticles"
        }) 
    else:
        return JsonResponse(
            {"status": "Error",
             "message": "HTTP method is not allowed"})

@csrf_exempt
def getArticle(request, id):
    if request.method == "GET":
        

        try:

            article = Article.objects.get(id=id)

            articleS = ArticleSerializer(article, many=False)

            return JsonResponse({
                "status": "success",
                "action": articleS.data
            })

        except Exception as e:
        
                return JsonResponse({
                    "status": "error",
                    "message": str(e)
            }) 
    else:
        return JsonResponse(
            {"status": "Error",
             "message": "HTTP method is not allowed"}, status=405)


@csrf_exempt
def deleteArticle(request, id):
    if request.method == "DELETE":

            try:

                article = Article.objects.get(id=id)

                article.delete()

                articleS = ArticleSerializer(article, many=False)

                return JsonResponse({
                    "status": "success",
                    "action": articleS.data
                })

            except Exception as e:
            
                    return JsonResponse({
                        "status": "error",
                        "message": str(e)
                }) 
    else:

        return JsonResponse(
            {"status": "Error",
            "message": "HTTP method is not allowed"}, status=405)


@csrf_exempt
def getArticlesByUser(request, userId):
    if request.method == "GET":
        
        articles = Article.objects.filter (user = userId)

        articlesS = ArticleSerializer(articles, many=True)

        return JsonResponse({
            "status": "Success",
            "articles": articlesS.data 
    }) 
    else:
        return JsonResponse(
            {"status": "Error",
             "message": "HTTP method is not allowed"}, status=405)

@csrf_exempt
def generateArticle(request, userId, theme):
    if request.method == "POST":

        # USAGE API KEY: OPEN AI
        client = OpenAI(api_key = settings.OPENAI_API_KEY)

        promptSystem = f"""
                You're a writter especialized on {theme}.
                User will ask to you for redact an article based on the theme.
                Any other theme is not allowed.

                Output must be (JSON):
                {
                    "title": "title,
                    "content": "content"
                }
            """
        
        promptUser = f"I need you to redact an article of {theme}"


        try:
            response = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = [
                    {"role": "system", "content": promptSystem},
                    {"role": "user", "content": promptUser}
                ],
                max_tokens =700,
                response_format={"type": "json_object"}
            )

            article_data = json.loads(response.choices[0].message.content)

            user = getattr(request, user)
            user_id = request.user['id']

            article_data["user_id"] = user_id

            article = Article.objects.create(**article_data)

            articleS = ArticleSerializer(article, many=False)

            return JsonResponse({
                "status": "success",
                "message": str(e)
            })

        except Exception as e:
                return JsonResponse({
                    "status": "error",
                    "message": str(e)
        
            }) 
    else:
        return JsonResponse(
            {"status": "Error",
             "message": "HTTP method is not allowed"})