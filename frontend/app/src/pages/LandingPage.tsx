import { useState } from 'react';
import { Button, Col, Container, Row } from 'react-bootstrap';
import { LandingPageCard } from '../components/LandingPageCard';
import { LogInModal } from '../components/LogInModal';
import styles from '../styles/LandingPage.module.css';


export function LandingPage() {
    const [logInModalShow, setLogInModalShow] = useState(false);

    const handleLogInModalClose = () => setLogInModalShow(false);
    const handleLogInModalShow = () => setLogInModalShow(true);

    return (
        <div className={`${styles.main_container}`}>
            <Container className={`${styles.top_container}`}>
                <Row>
                    <Col xs={8}>
                        <div className={`${styles.main_title}`}>CookTOP</div>
                        <div className="px-3">
                            <h2>Make cooking cheaper and faster.</h2>
                        </div>
                    </Col>
                    <Col
                        xs={4}
                        className="d-flex justify-content-end flex-wrap align-items-center"
                    >
                        <Button
                            className="mx-3 mb-3 mt-auto"
                            onClick={handleLogInModalShow}
                        >
                            {'Log In'}
                        </Button>
                        <Button className="mx-3 mb-3 mt-auto">{'Sign Up'}</Button>
                        <LogInModal
                            show={logInModalShow}
                            handleClose={handleLogInModalClose}
                        />
                    </Col>
                </Row>
            </Container>
            <Container>
                <Row md={4} sm={2} xs={2} gap={4} className="m-4">
                    <Col className="d-flex">
                        <LandingPageCard
                            title={'Smart Meal Planning'}
                            text={
                                'Generate meal plans with\
                                 recipes that use items you already have in your pantry.\
                                 You can also request items, so you make the best use of\
                                 discounts at your local grocery store.'
                            }
                        />
                    </Col>
                    <Col className="d-flex">
                        <LandingPageCard
                            title={'Recipe Storage'}
                            text={
                                'Add your favorite recipes to your account.\
                                 It\'s fast! You can add recipes from the web in a\
                                 a few seconds. Once you add your recipes, you can\
                                 quickly find recipes by tags or ingredients.'
                            }
                        />
                    </Col>
                    <Col className="d-flex">
                        <LandingPageCard
                            title={'Pantry Management'}
                            text={
                                'Don\'t worry about food going bad in your fridge anymore.\
                                 Add the items your have and their expiration date.\
                                 Then CookTOP will manage to include them in your plans\
                                 while your food is still good.'
                            }
                        />
                    </Col>
                    <Col className="d-flex">
                        <LandingPageCard
                            title={'Grocery Shopping'}
                            text={
                                'After a meal plan is generated, the items you don\'t have in\
                                 your pantry can be added to your shopping list automatically.\
                                 It\'s also possible to edit the shopping list manually.'
                            }
                        />
                    </Col>
                </Row>
            </Container>
        </div>
    );
}
