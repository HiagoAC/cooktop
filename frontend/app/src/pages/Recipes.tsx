import { Button, Row, Col } from 'react-bootstrap';
import { recipes, RecipeListInfo } from '../data/recipes';
import { RecipeInList } from '../components/RecipeInList';
import '../styles/Recipes.css';

export function Recipes() {
    return (
        <>
            <div className="page-title mt-3">Recipes</div>
            <Row className="justify-content-md-center g-6">
                <Col className="button-col mt-2 mb-5">
                    <Button href="/recipes" className="mx-4 custom-button">
                        My Recipes
                    </Button>
                    <Button href="/recipes/add" className="mx-4 custom-button">
                        Add Recipe
                    </Button>
                    <Button href="/recipes/search" className="mx-4 custom-button">
                        Search
                    </Button>
                </Col>
            </Row>
            <Row lg={3} md={2} xs={1} className="g-4">
                {recipes.map((recipe: RecipeListInfo) => (
                    <Col key={recipe.id}><RecipeInList {...recipe} /></Col>
                ))}
            </Row>
        </>
    )
}
