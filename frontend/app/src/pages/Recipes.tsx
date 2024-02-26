import { Button, Row, Col, Container } from 'react-bootstrap';
import { recipes, RecipeListInfo } from '../data/recipes';
import { RecipeInList } from '../components/RecipeInList';
import styles from '../styles/Recipes.module.css';


export function Recipes() {
    return (
        <Container className="pb-4">
            <div className="page_title mt-3">Recipes</div>
            <Row className="justify-content-md-center g-6">
                <Col className={`mt-2 mb-5 ${styles.button_col}`}>
                    <Button href="/recipes" className="mx-4 custom_button">
                        My Recipes
                    </Button>
                    <Button href="/recipes/add" className="mx-4 custom_button">
                        Add Recipe
                    </Button>
                    <Button href="/recipes/search" className="mx-4 custom_button">
                        Search
                    </Button>
                </Col>
            </Row>
            <Row lg={4} md={2} xs={1} className="g-4">
                {recipes.map((recipe: RecipeListInfo) => (
                    <Col key={recipe.id}><RecipeInList {...recipe} /></Col>
                ))}
            </Row>
        </Container>
    )
}
