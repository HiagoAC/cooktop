import { Button, Row, Col, Container } from 'react-bootstrap';
import { RecipeListInfo } from '../api/apiSchemas/recipesSchemas';
import { getRecipes } from '../api/recipesApi';
import { RecipeInList } from '../components/RecipeInList';
import styles from '../styles/Recipes.module.css';
import { useEffect, useState } from 'react';


export function Recipes() {
    const [recipes, setRecipes] = useState<RecipeListInfo[]>([]);

    useEffect(() => {
        const fetchRecipes = async () => {
            getRecipes().then(res => {
                if (res.status === 200) {
                    setRecipes(res.data);
                } else {
                    console.log('Failed to fetch recipes');
                }
            });
        };
        fetchRecipes();
    }, []);
    
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
