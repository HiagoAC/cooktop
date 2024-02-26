import { Card, Container, ListGroup } from "react-bootstrap";

export function About() {
    return (
        <Container className="pb-4 mx-5 px-5">
            <div className="page_title my-3">About CookTOP</div>
            <Card body className="mb-3">
                <Card.Text>
                    {'Cooktop is a meal planning tool developed to make everyday \
                      cooking cheaper, faster and more efficient. It generates \
                      meal plans that help users minimize food wastage while \
                      reducing both cooking and grocery shopping time. In \
                      addition to meal planning, Cooktop also integrates \
                      recipe, grocery shopping, and pantry management into a \
                      single application.'}
                </Card.Text>
            </Card>
            <Card body className="mb-3">
                <Card.Title>{'Managing Recipes'}</Card.Title>
                <Card.Text>
                    {'With Cooktop you can keep your favorite recipes in your \
                      personal account. You can choose to add recipes manually \
                      or you can add recipes you found online automatically. \
                      You just have to enter the URL of the recipe. Then, you \
                      can query for recipes based on ingredients, cooking time, \
                      tags, etc. It is also possible to delete or edit your \
                      recipes at anytime.'}
                </Card.Text>
            </Card>
            <Card body className="mb-3">
                <Card.Title>{'Managing Pantry'}</Card.Title>
                <Card.Text>
                    {'In the pantry section, you can keep track of what you have in \
                      stock. When adding items, you have the option to include an \
                      expiration date to it. So, expiring ingredients can be \
                      prioritized in the meal plans. The quantity of ingredients \
                      in the pantry can also be adjusted automatically based on \
                      the groceries you buy and what is used in your meals.'}
                </Card.Text>
            </Card>
            <Card body className="mb-3">
                <Card.Title>{'Generating Meal Plans'}</Card.Title>
                <Card.Text>
                    {'This feature was the main motivation for building this \
                      application. You select how many times you want to cook, \
                      how many servings you need, and ingredients you want to \
                      use. Then, Cooktop generates a plan based on that and \
                      your pantry. The app finds a variety of recipes while \
                      trying to reuse as many ingredients as possible especially \
                      those already in your pantry. It is also possible to \
                      replace recipes once the plan is ready if you wish. There \
                      are several reasons to planning meals this way:'}
                      <ListGroup>
                        <ListGroup.Item>
                            <strong>{'Reducing shopping time: '}</strong>
                            {'You save time shopping because \
                              there are fewer things you have to buy. This is because \
                              you will already have many of the ingredients in the \
                              plan, and you can purchase other ingredients in larger \
                              quantities since they are being used in several recipes.'}
                        </ListGroup.Item>
                        <ListGroup.Item>
                            <strong>{'Reducing food wastage: '}</strong>
                            {'Cooking food with a great variety \
                              of ingredients and having a large amount of unused items \
                              increases the chances of food spoilage. This plan minimizes \
                              this.'}
                        </ListGroup.Item>
                        <ListGroup.Item>
                            <strong>{'Saving cooking time: '}</strong>
                            {'Reusing ingredients means there are \
                              higher chances of batch cooking. For example, the same may \
                              be chopped or marinate in the different recipes. You can \
                              do it when you cook the first meal and not have to do it \
                              again when cooking the second one on another day.'}
                        </ListGroup.Item>
                        <ListGroup.Item>
                            <strong>{'Saving money: '}</strong>
                            {'Besides saving money by reducing waste. \
                              You can also cut your grocery spending. You can select \
                              ingredients to be used in the plan and their quantities. \
                              So you can make better use of discounts in your grocery \
                              store.'}
                        </ListGroup.Item>
                      </ListGroup>
                </Card.Text>
            </Card>
            <Card body className="mb-3">
                <Card.Title>{'Generating Shopping List'}</Card.Title>
                <Card.Text>
                    {'Once the weekly meal plan is established, Cooktop automatically \
                      generates a corresponding shopping list. Additionally, users \
                      have the flexibility to manually edit the list according to \
                      their preferences.'}
                </Card.Text>
            </Card>
        </Container>
    );
}
