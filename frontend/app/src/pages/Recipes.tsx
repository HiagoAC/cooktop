import { Button, Row, Col } from 'react-bootstrap';
import recipes from '../data/recipes.json';
import { RecipeInList } from '../components/RecipeInList';
import '../styles/Recipes.css';

export function Recipes() {
    return (
        <>
            <div className="page-title mt-3">Recipes</div>
            <Row className="justify-content-md-center g-6">
                <Col className="button-col mt-2 mb-5">
                    {['My Recipes', 'Add Recipe', 'Search'].map(text => (
                        <Button className="mx-4 custom-button">{text}</Button>
                    ))}
                </Col>
            </Row>
            <Row lg={3} md={2} xs={1} className="g-4">
                {recipes.map(recipe => (
                    <Col key={recipe.id}><RecipeInList {...recipe} /></Col>
                ))}
            </Row>
        </>
    )
}
